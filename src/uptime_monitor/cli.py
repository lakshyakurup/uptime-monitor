from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from .checker import check_targets, read_targets_file, summarize_results
from .config import load_config
from .logging_utils import configure_logging
from .notifier import write_summary
from .organizer import organize_files
from .scheduler import run_periodic

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    defaults = load_config()
    parser = argparse.ArgumentParser(description="Uptime monitor toolkit")
    parser.add_argument("--log-level", default=defaults.log_level, help="Logging level")

    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Check URLs")
    check.add_argument("--targets-file", default=str(defaults.targets_file), help="Path to targets file")
    check.add_argument("--timeout", type=float, default=defaults.timeout_seconds, help="Request timeout")
    check.add_argument("--user-agent", default=defaults.user_agent, help="User-Agent header")

    notify = sub.add_parser("notify", help="Write a notification summary")
    notify.add_argument("--output", default=str(defaults.summary_output_file), help="Summary output file")
    notify.add_argument("--title", default="System Update")
    notify.add_argument("--message", default="Automation task completed")
    notify.add_argument("--status", default="OK")

    organize = sub.add_parser("organize", help="Organize files by extension")
    organize.add_argument("source", help="Source directory")
    organize.add_argument("--destination", default="organized_files", help="Destination directory")
    organize.add_argument("--dry-run", action="store_true")

    run = sub.add_parser("run", help="Run check and summary together")
    run.add_argument("--targets-file", default=str(defaults.targets_file), help="Path to targets file")
    run.add_argument("--timeout", type=float, default=defaults.timeout_seconds)
    run.add_argument("--user-agent", default=defaults.user_agent)
    run.add_argument("--output", default=str(defaults.summary_output_file))
    run.add_argument("--title", default="Uptime Check")
    run.add_argument("--interval", type=int, default=defaults.interval_seconds)
    run.add_argument("--iterations", type=int, default=1)

    return parser


def _run_check(targets_file: str, timeout: float, user_agent: str) -> tuple[int, int]:
    urls = read_targets_file(Path(targets_file))
    results = check_targets(urls, timeout_seconds=timeout, user_agent=user_agent)
    for item in results:
        if item.ok:
            print(f"[ONLINE] {item.url} - Status: {item.status_code} - Response Time: {item.latency_ms}ms")
        else:
            print(f"[OFFLINE] {item.url} - Error: {item.error}")
    return summarize_results(results)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.log_level)

    if args.command == "check":
        try:
            _run_check(args.targets_file, args.timeout, args.user_agent)
            return 0
        except FileNotFoundError:
            logger.error("Targets file not found: %s", args.targets_file)
            return 1

    if args.command == "notify":
        written = write_summary(Path(args.output).expanduser().resolve(), args.title, args.message, args.status)
        print(f"Notification summary written to {written}")
        return 0

    if args.command == "organize":
        source = Path(args.source).expanduser().resolve()
        destination = Path(args.destination).expanduser().resolve()
        if source == destination:
            parser.error("Source and destination must be different directories")
        try:
            moved_files = organize_files(source, destination, dry_run=args.dry_run)
        except (FileNotFoundError, NotADirectoryError) as exc:
            parser.exit(status=1, message=f"Error: {exc}\n")
            return 1

        if args.dry_run:
            print(f"Dry run complete. {len(moved_files)} file(s) would be moved.")
        else:
            print(f"Organization complete. {len(moved_files)} file(s) moved.")

        for name, location in moved_files:
            print(f"- {name} -> {location}")
        return 0

    if args.command == "run":
        def run_once() -> None:
            online, offline = _run_check(args.targets_file, args.timeout, args.user_agent)
            status = "OK" if offline == 0 else "WARNING"
            message = f"Uptime check completed. Online: {online}, Offline: {offline}."
            write_summary(Path(args.output).expanduser().resolve(), args.title, message, status)

        run_periodic(run_once, interval_seconds=args.interval, iterations=args.iterations)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

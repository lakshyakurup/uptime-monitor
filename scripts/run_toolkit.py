#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

def run_cmd(cmd: list[str]) -> int:
    print(f"\n[RUN] {' '.join(cmd)}")
    return subprocess.call(cmd)

def main():
    p = argparse.ArgumentParser(description="Automation Toolkit Runner")
    p.add_argument("--targets", default="targets.txt", help="Targets file (one URL per line).")
    p.add_argument("--workdir", default="./workspace", help="Where outputs will be written.")
    args = p.parse_args()

    workdir = Path(args.workdir).resolve()
    uptime_dir = workdir / "uptime"
    notify_dir = workdir / "notifications"
    organized_dir = workdir / "organized"

    uptime_dir.mkdir(parents=True, exist_ok=True)
    notify_dir.mkdir(parents=True, exist_ok=True)
    organized_dir.mkdir(parents=True, exist_ok=True)

    # 1) Uptime + notification summary
    # Update these paths if your filenames are different in scripts/
    summary_script = "scripts/notification_summary.py"
    notify_out = notify_dir / "notification_summary.txt"

    ret = run_cmd([
        "python3", summary_script,
        "--targets", args.targets,
        "--output", str(notify_out)
    ])
    if ret != 0:
        print("[WARN] notification_summary.py exited with non-zero code. Continuing...")

    # 2) Organize output files
    organizer_script = "scripts/organize_files.py"
    ret2 = run_cmd([
        "python3", organizer_script,
        str(workdir),
        str(organized_dir)
    ])
    if ret2 != 0:
        raise SystemExit(ret2)

    print("\n✅ Toolkit run complete!")
    print(f"Targets: {Path(args.targets).resolve()}")
    print(f"Notification: {notify_out}")

if __name__ == "__main__":
    main()

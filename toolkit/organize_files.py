#!/usr/bin/env python3
"""Organize files in a directory by file extension."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def extension_bucket(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    return suffix if suffix else "no_extension"


def organize_directory(directory: Path, dry_run: bool = False) -> dict[str, int]:
    moved: dict[str, int] = {}

    for item in directory.iterdir():
        if not item.is_file():
            continue

        bucket = extension_bucket(item)
        target_dir = directory / bucket
        target_path = target_dir / item.name

        if item.parent == target_dir:
            continue

        moved[bucket] = moved.get(bucket, 0) + 1

        if dry_run:
            continue

        target_dir.mkdir(exist_ok=True)
        shutil.move(str(item), str(target_path))

    return moved


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without modifying files",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    directory = Path(args.directory).expanduser().resolve()
    if not directory.exists() or not directory.is_dir():
        parser.error(f"Invalid directory: {directory}")

    moved = organize_directory(directory, dry_run=args.dry_run)

    if not moved:
        print("No files to organize.")
        return 0

    total = sum(moved.values())
    mode = "Would move" if args.dry_run else "Moved"
    print(f"{mode} {total} file(s):")
    for file_type, count in sorted(moved.items()):
        print(f"  - {file_type}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

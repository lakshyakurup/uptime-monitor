#!/usr/bin/env python3
"""Organize files in a directory by file type."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import List, Tuple


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Move files from a source folder into subfolders based on file extension."
    )
    parser.add_argument("source", help="Directory containing files to organize")
    parser.add_argument(
        "--destination",
        default="organized_files",
        help="Directory where organized files will be placed (default: organized_files)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving any files",
    )
    return parser


def organize_files(source: Path, destination: Path, dry_run: bool = False) -> List[Tuple[str, str]]:
    if not source.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    moved_files: List[Tuple[str, str]] = []
    for path in sorted(source.iterdir()):
        if not path.is_file():
            continue

        extension = path.suffix.lower().lstrip(".") or "no_extension"
        target_folder = destination / extension
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / path.name
        counter = 1
        while target_path.exists():
            new_name = f"{path.stem}_{counter}{path.suffix}"
            target_path = target_folder / new_name
            counter += 1

        if dry_run:
            moved_files.append((path.name, target_path.relative_to(destination).as_posix()))
            continue

        shutil.move(str(path), str(target_path))
        moved_files.append((path.name, target_path.relative_to(destination).as_posix()))

    return moved_files


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    destination = Path(args.destination).expanduser().resolve()

    if source == destination:
        parser.error("Source and destination must be different directories")

    try:
        moved_files = organize_files(source, destination, dry_run=args.dry_run)
    except (FileNotFoundError, NotADirectoryError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    if args.dry_run:
        print(f"Dry run complete. {len(moved_files)} file(s) would be moved.")
    else:
        print(f"Organization complete. {len(moved_files)} file(s) moved.")

    for name, location in moved_files:
        print(f"- {name} -> {location}")


if __name__ == "__main__":
    main()

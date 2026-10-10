from __future__ import annotations

import shutil
from pathlib import Path


def organize_files(source: Path, destination: Path, dry_run: bool = False) -> list[tuple[str, str]]:
    if not source.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    moved_files: list[tuple[str, str]] = []
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

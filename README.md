# uptime-monitor

Simple Python automation toolkit with command-line scripts for:

- organizing files by type (file extension)
- writing notification summaries to a local text file

## Setup

1. Ensure Python 3.9+ is installed.
2. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No third-party dependencies are required.

## Usage

### 1) Organize files by type

Script: `/home/runner/work/uptime-monitor/uptime-monitor/toolkit/organize_files.py`

```bash
python3 /home/runner/work/uptime-monitor/uptime-monitor/toolkit/organize_files.py /path/to/folder
```

Options:

- `--dry-run` prints what would be moved without changing files.

Example:

```bash
python3 /home/runner/work/uptime-monitor/uptime-monitor/toolkit/organize_files.py . --dry-run
```

### 2) Write a notification summary to a local text file

Script: `/home/runner/work/uptime-monitor/uptime-monitor/toolkit/write_notification.py`

```bash
python3 /home/runner/work/uptime-monitor/uptime-monitor/toolkit/write_notification.py "File Organizer" "Moved 14 files into extension folders"
```

Options:

- `--output` sets a custom output text file path (default: `notifications.txt`).

Example:

```bash
python3 /home/runner/work/uptime-monitor/uptime-monitor/toolkit/write_notification.py "Daily Summary" "No files needed organizing" --output ./logs/notifications.txt
```

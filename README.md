# Uptime Monitor Automation Toolkit

This workspace now includes a small Python-based automation toolkit with a command-line interface. It contains two sample scripts:

- organize_files.py: moves files from a source folder into subfolders based on file type
- notification_summary.py: writes a short notification summary to a local text file

## Setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment (optional but recommended):
   - python3 -m venv .venv
   - source .venv/bin/activate
3. Install dependencies if needed:
   - pip install -r requirements.txt

## Usage

### Organize files by type

Run the file organizer against a folder:

```bash
python3 scripts/organize_files.py /path/to/source --destination /path/to/output
```

Use the dry-run flag to preview changes without moving files:

```bash
python3 scripts/organize_files.py /path/to/source --dry-run
```

### Send a notification summary to a local text file

Create a summary file with a title, message, and status:

```bash
python3 scripts/notification_summary.py --output notifications/summary.txt --title "Daily Check" --message "Automation completed successfully" --status OK
```

## Example

```bash
python3 scripts/organize_files.py ./sample_files --dry-run
python3 scripts/notification_summary.py --output ./output/summary.txt
```

## Notes

- The organizer uses the file extension to decide where files are placed.
- If a destination file already exists, the script appends a numeric suffix to avoid overwriting files.
- The notification script writes UTF-8 text and creates parent folders automatically.

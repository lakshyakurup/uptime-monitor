from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def write_summary(output: Path, title: str, message: str, status: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = "\n".join(
        [
            f"Notification: {title}",
            f"Status: {status}",
            f"Time: {timestamp}",
            f"Message: {message}",
        ]
    )
    output.write_text(content + "\n", encoding="utf-8")
    return output

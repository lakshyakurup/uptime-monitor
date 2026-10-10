#!/usr/bin/env python3
"""Backward-compatible uptime checker script."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from uptime_monitor.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["check"]))

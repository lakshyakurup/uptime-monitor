#!/usr/bin/env python3
"""Backward-compatible file organizer script."""

from __future__ import annotations

import sys

from uptime_monitor.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["organize", *sys.argv[1:]]))

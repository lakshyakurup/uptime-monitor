#!/usr/bin/env python3
"""Backward-compatible notification summary script."""

from __future__ import annotations

import sys

from uptime_monitor.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["notify", *sys.argv[1:]]))

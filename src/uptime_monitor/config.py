from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    targets_file: Path = Path("targets.txt")
    timeout_seconds: float = 5.0
    user_agent: str = "UptimeMonitor/1.0"
    summary_output_file: Path = Path("output/notification_summary.txt")
    log_level: str = "INFO"
    interval_seconds: int = 0

    def validate(self) -> "AppConfig":
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than 0")
        if self.interval_seconds < 0:
            raise ValueError("interval_seconds must be 0 or greater")
        if not self.user_agent.strip():
            raise ValueError("user_agent cannot be empty")
        if self.log_level.upper() not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("log_level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL")
        return self


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> AppConfig:
    config = AppConfig(
        targets_file=Path(os.getenv("UPTIME_TARGETS_FILE", "targets.txt")),
        timeout_seconds=float(os.getenv("UPTIME_TIMEOUT_SECONDS", "5")),
        user_agent=os.getenv("UPTIME_USER_AGENT", "UptimeMonitor/1.0"),
        summary_output_file=Path(
            os.getenv("UPTIME_SUMMARY_OUTPUT_FILE", "output/notification_summary.txt")
        ),
        log_level=os.getenv("UPTIME_LOG_LEVEL", "INFO"),
        interval_seconds=int(os.getenv("UPTIME_INTERVAL_SECONDS", "0")),
    )
    _env_bool("UPTIME_VERBOSE_LOGS", default=False)
    return config.validate()

from __future__ import annotations

import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CheckResult:
    url: str
    status_code: int | None
    latency_ms: float | None
    error: str | None
    checked_at: datetime

    @property
    def ok(self) -> bool:
        return self.error is None and self.status_code is not None and self.status_code < 400


def read_targets_file(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def check_url(url: str, timeout_seconds: float, user_agent: str) -> CheckResult:
    checked_at = datetime.now(timezone.utc)
    try:
        start = time.perf_counter()
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:  # noqa: S310
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return CheckResult(
                url=url,
                status_code=getattr(response, "status", 200),
                latency_ms=latency_ms,
                error=None,
                checked_at=checked_at,
            )
    except Exception as exc:  # noqa: BLE001
        return CheckResult(
            url=url,
            status_code=None,
            latency_ms=None,
            error=str(exc),
            checked_at=checked_at,
        )


def check_targets(urls: Iterable[str], timeout_seconds: float, user_agent: str) -> list[CheckResult]:
    return [check_url(url.strip(), timeout_seconds, user_agent) for url in urls if url.strip()]


def summarize_results(results: Iterable[CheckResult]) -> tuple[int, int]:
    result_list = list(results)
    online = sum(1 for item in result_list if item.ok)
    return online, len(result_list) - online

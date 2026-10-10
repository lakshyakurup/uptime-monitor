from __future__ import annotations

import logging
import time
from collections.abc import Callable


def run_periodic(task: Callable[[], None], interval_seconds: int, iterations: int | None = None) -> None:
    logger = logging.getLogger(__name__)
    count = 0
    while True:
        try:
            task()
        except Exception:  # noqa: BLE001
            logger.exception("Scheduled task failed")
        count += 1
        if iterations is not None and count >= iterations:
            break
        if interval_seconds <= 0:
            break
        time.sleep(interval_seconds)

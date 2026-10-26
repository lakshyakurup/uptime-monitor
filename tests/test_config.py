import pytest

from uptime_monitor.config import load_config


def test_load_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UPTIME_TIMEOUT_SECONDS", "10")
    monkeypatch.setenv("UPTIME_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("UPTIME_INTERVAL_SECONDS", "30")

    config = load_config()

    assert config.timeout_seconds == 10
    assert config.log_level == "DEBUG"
    assert config.interval_seconds == 30


def test_load_config_validates_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UPTIME_TIMEOUT_SECONDS", "0")
    with pytest.raises(ValueError):
        load_config()

from pathlib import Path

from uptime_monitor.checker import read_targets_file, summarize_results, check_targets


def test_read_targets_file_skips_blanks_and_comments(tmp_path: Path) -> None:
    targets = tmp_path / "targets.txt"
    targets.write_text("\n# comment\nhttps://example.com\n\nhttps://github.com\n", encoding="utf-8")

    assert read_targets_file(targets) == ["https://example.com", "https://github.com"]


def test_check_targets_handles_unreachable_url() -> None:
    results = check_targets(["http://127.0.0.1:1"], timeout_seconds=0.001, user_agent="test-agent")

    online, offline = summarize_results(results)
    assert online == 0
    assert offline == 1

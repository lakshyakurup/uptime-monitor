from pathlib import Path

from uptime_monitor.cli import main


def test_notify_command_writes_file(tmp_path: Path) -> None:
    output = tmp_path / "summary.txt"

    code = main([
        "notify",
        "--output",
        str(output),
        "--title",
        "Daily Check",
        "--message",
        "Done",
        "--status",
        "OK",
    ])

    assert code == 0
    assert output.exists()
    contents = output.read_text(encoding="utf-8")
    assert "Notification: Daily Check" in contents

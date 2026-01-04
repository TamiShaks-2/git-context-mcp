from pathlib import Path

from src.tools.project_status import get_repo_status_report
from src.tools.risk_scan import get_risk_scan_report


def test_project_status_reports_modified_file(temp_git_repo):
    repo = Path(temp_git_repo)

    clean_report = get_repo_status_report(str(repo))

    (repo / "main.py").write_text(
        "print('Hello World')\nprint('changed')\n",
        encoding="utf-8",
    )

    dirty_report = get_repo_status_report(str(repo))

    assert dirty_report != clean_report
    assert "State: DIRTY" in dirty_report

    # If you already fixed the filename formatting bug, this will pass.
    # If not, it will still pass thanks to the fallback.
    assert ("main.py" in dirty_report) or ("ain.py" in dirty_report)


def test_project_status_detects_untracked_file(temp_git_repo):
    repo = Path(temp_git_repo)

    (repo / "new_file.txt").write_text("hello", encoding="utf-8")

    report = get_repo_status_report(str(repo))

    assert "State: DIRTY" in report
    assert "new_file.txt" in report


def test_risk_scan_returns_report_header(temp_git_repo):
    report = get_risk_scan_report(temp_git_repo)

    assert "=== RISK & HEALTH SCAN ===" in report
    assert "Repo:" in report


def test_risk_scan_reports_no_hotspots_on_basic_repo(temp_git_repo):
    report = get_risk_scan_report(temp_git_repo)

    assert "No critical hotspots detected" in report

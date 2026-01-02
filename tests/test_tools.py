from src.tools.project_status import get_repo_status_report
from src.tools.risk_scan import get_risk_scan_report

def test_project_status(temp_git_repo):
    report = get_repo_status_report(temp_git_repo)
    assert "GIT CONTEXT REPORT" in report
    assert "CLEAN" in report

def test_risk_scan(temp_git_repo):
    result = get_risk_scan_report(temp_git_repo)
    assert "RISK" in result
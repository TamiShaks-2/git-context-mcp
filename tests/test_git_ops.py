from src.tools.git_ops import run_git_cmd
from pathlib import Path

def test_git_cmd_success(temp_git_repo):
    output = run_git_cmd(Path(temp_git_repo), ["status"])
    assert "branch" in output

def test_git_cmd_grep_missing(temp_git_repo):
    """Test that missing grep results return empty string, not None/crash."""
    output = run_git_cmd(Path(temp_git_repo), ["grep", "MISSING_STRING"])
    assert output == ""

def test_git_cmd_invalid(temp_git_repo):
    output = run_git_cmd(Path(temp_git_repo), ["not-a-command"])
    assert output == ""
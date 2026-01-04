import pytest
import subprocess
from pathlib import Path

@pytest.fixture
def temp_git_repo(tmp_path):
    """
    Creates a temporary git repository with dummy content.
    Returns the path to the repo.
    """
    repo_path = tmp_path / "dummy_repo"
    repo_path.mkdir()
    
    # Basic git config so the test doesn't fail on "who are you"
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@bot.com"], cwd=repo_path)
    subprocess.run(["git", "config", "user.name", "Test Bot"], cwd=repo_path)
    
    # Create dummy files
    (repo_path / "main.py").write_text("print('Hello World')")
    (repo_path / "utils.py").write_text("# TODO: Refactor this\ndef util(): pass")
    
    # First commit
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)
    
    return str(repo_path)
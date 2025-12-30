import subprocess
import os
from pathlib import Path
from typing import List

def run_git_cmd(cwd: Path, args: List[str]) -> str:
    """Executes a git command safely and returns stdout."""
    # Print to terminal so we can see what's happening in real time
    print(f"--- Running git command: {' '.join(args)} in {cwd}")
    
    # Environment settings to avoid hangs on Windows
    env = os.environ.copy()
    env["GIT_PAGER"] = "cat"      # prevents opening an editor
    env["GIT_TERMINAL_PROMPT"] = "0" # prevents password prompts

    try:
        # added stdin=subprocess.DEVNULL so it won't wait for input
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            stdin=subprocess.DEVNULL, 
            env=env
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"!!! Command failed: {e}")
        return ""
    except Exception as e:
        print(f"!!! Unexpected error: {e}")
        raise

def get_repo_status_report(repo_path: str) -> str:
    print(f"Starting report for: {repo_path}")
    path = Path(repo_path).resolve()
    
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."
    
    # 1. Branch
    print("Step 1: Checking Branch...")
    branch = run_git_cmd(path, ["branch", "--show-current"]) or "DETACHED_HEAD"
    
    # 2. Status
    print("Step 2: Checking Status...")
    status_raw = run_git_cmd(path, ["status", "--porcelain"])
    uncommitted = bool(status_raw)
    
    changes_summary = []
    if uncommitted:
        for line in status_raw.splitlines():
            if len(line) > 3:
                code = line[:2]
                fname = line[3:]
                changes_summary.append(f"  [{code}] {fname}")

    # 3. Sync Status (this is usually where problems occur)
    print("Step 3: Checking Sync with Origin...")
    ahead, behind = 0, 0
    # Check if 'origin' exists first to avoid running a heavy command unnecessarily
    remotes = run_git_cmd(path, ["remote"]) 
    
    if "origin" in remotes:
        # This command can sometimes hang if there's no network or git is outdated
        sync_raw = run_git_cmd(path, ["rev-list", "--left-right", "--count", "origin/main...HEAD"])
        if sync_raw:
            try:
                b_str, a_str = sync_raw.split()
                behind, ahead = int(b_str), int(a_str)
            except ValueError:
                pass
    else:
        print("No origin found, skipping sync check.")

    print("Step 4: Building Report...")
    # Build Report
    report = [
        f"=== GIT CONTEXT REPORT ===",
        f"Repo: {path.name}",
        f"Path: {path}",
        f"Branch: {branch}",
        f"State: {'DIRTY' if uncommitted else 'CLEAN'}"
    ]

    if ahead or behind:
        report.append(f"Sync: +{ahead} (ahead) / -{behind} (behind) origin/main")
    
    if changes_summary:
        report.append("\nChanges:")
        report.extend(changes_summary[:20])
            
    return "\n".join(report)
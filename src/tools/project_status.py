from pathlib import Path
from .git_ops import run_git_cmd

def get_repo_status_report(repo_path: str) -> str:
    """Generates a technical snapshot of the repo state."""
    path = Path(repo_path).resolve()
    
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."
    
    # 1. Branch
    branch = run_git_cmd(path, ["branch", "--show-current"]) or "DETACHED_HEAD"
    
    # 2. Status
    status_raw = run_git_cmd(path, ["status", "--porcelain"])
    uncommitted = bool(status_raw)
    
    changes_summary = []
    if uncommitted:
        for line in status_raw.splitlines():
            if len(line) > 3:
                code = line[:2]
                fname = line[3:]
                changes_summary.append(f"  [{code}] {fname}")

    # 3. Sync Status
    ahead, behind = 0, 0
    remotes = run_git_cmd(path, ["remote"]) 
    
    if "origin" in remotes:
        sync_raw = run_git_cmd(path, ["rev-list", "--left-right", "--count", "origin/main...HEAD"])
        if sync_raw:
            try:
                b_str, a_str = sync_raw.split()
                behind, ahead = int(b_str), int(a_str)
            except ValueError:
                pass

    # Build Report
    report = [
        f"=== GIT CONTEXT REPORT ===",
        f"Repo: {path.name}",
        f"Path: {path}",
        f"Branch: {branch}",
        f"State: {'DIRTY (Unsaved changes)' if uncommitted else 'CLEAN'}"
    ]

    if ahead or behind:
        report.append(f"Sync: +{ahead} (ahead) / -{behind} (behind) origin/main")
    
    if changes_summary:
        report.append("\nChanges:")
        report.extend(changes_summary[:20])
            
    return "\n".join(report)
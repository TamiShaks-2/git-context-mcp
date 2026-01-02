from pathlib import Path
from collections import Counter
from .git_ops import run_git_cmd

def get_recent_activity_report(repo_path: str, n: int = 20) -> str:
    """Generates a report on recent commits and hot files."""
    path = Path(repo_path).resolve()
    
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    # 1. Recent Commits Log
    log_fmt = "%h|%an|%ar|%s"
    commits_raw = run_git_cmd(path, ["log", f"-n {n}", f"--pretty=format:{log_fmt}"])
    
    commits_report = []
    if commits_raw:
        for line in commits_raw.splitlines():
            parts = line.split("|")
            if len(parts) >= 4:
                h, author, time, msg = parts[0], parts[1], parts[2], parts[3]
                commits_report.append(f"  * {h} ({time}) {author}: {msg}")
    
    # 2. Identify "Hot" Files
    files_raw = run_git_cmd(path, ["log", f"-n {n}", "--name-only", "--format="])
    
    hot_files_report = []
    if files_raw:
        files = [f.strip() for f in files_raw.splitlines() if f.strip()]
        if files:
            counter = Counter(files)
            most_common = counter.most_common(5)
            hot_files_report.append(f"Top Modified Files (Last {n} commits):")
            for fname, count in most_common:
                hot_files_report.append(f"  - {fname} ({count} changes)")
    
    report = [
        f"=== RECENT ACTIVITY REPORT (Last {n} commits) ===",
        f"Repo: {path.name}",
        ""
    ]
    
    if hot_files_report:
        report.extend(hot_files_report)
        report.append("")
        
    if commits_report:
        report.append("Recent Commits:")
        report.extend(commits_report)

    return "\n".join(report)
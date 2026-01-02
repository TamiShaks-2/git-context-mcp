from pathlib import Path
from collections import Counter
from .git_ops import run_git_cmd

def get_work_summary(repo_path: str, since: str = "7d") -> str:
    """Analyzes work done since a specific time and scans for technical debt."""
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    report = [f"=== WORK SUMMARY (Since: {since}) ===", f"Repo: {path.name}"]

    # 1. Activity Overview
    changed_files_raw = run_git_cmd(path, ["log", f"--since={since}", "--name-only", "--format="])
    files = [f.strip() for f in changed_files_raw.splitlines() if f.strip()]
    
    report.append(f"\nActivity Overview:")
    report.append(f"  - Total files touched: {len(set(files))}")
    
    # 2. Active Modules
    if files:
        modules = []
        for f in files:
            p = Path(f)
            if len(p.parts) > 1:
                modules.append(str(p.parent))
            else:
                modules.append("Root")
        
        module_counts = Counter(modules).most_common(5)
        report.append("  - Most Active Modules/Folders:")
        for mod, count in module_counts:
            report.append(f"    * {mod} ({count} updates)")

    # 3. TODO / FIXME Scan
    report.append(f"\nTechnical Debt Scan (TODOs / FIXMEs):")
    try:
        grep_output = run_git_cmd(path, ["grep", "-I", "-n", "-E", "TODO|FIXME"])
        if grep_output:
            lines = grep_output.splitlines()
            report.append(f"  Found {len(lines)} items. Top items:")
            for line in lines[:10]:
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    fname, linenum, content = parts[0], parts[1], parts[2].strip()
                    if len(content) > 60: content = content[:57] + "..."
                    report.append(f"    [Line {linenum}] {fname}: {content}")
        else:
            report.append("  Good job! No TODOs found.")
    except Exception:
        report.append("  (Could not scan for TODOs)")

    return "\n".join(report)
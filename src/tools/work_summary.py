from pathlib import Path
from collections import Counter
from .git_ops import run_git_cmd

def get_work_summary(repo_path: str, since: str = "7d") -> str:
    """
    Analyzes work done since a specific time and scans for technical debt.
    """
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    report = [f"=== WORK SUMMARY (Since: {since}) ===", f"Repo: {path.name}"]

    # --- 1. Changes Overview (What changed?) ---
    # Ask git only for the names of files changed in this period
    changed_files_raw = run_git_cmd(path, ["log", f"--since={since}", "--name-only", "--format="])
    
    files = [f.strip() for f in changed_files_raw.splitlines() if f.strip()]
    total_files_changed = len(set(files))
    
    report.append(f"\nActivity Overview:")
    report.append(f"  - Total files touched: {total_files_changed}")
    
    # --- 2. Active Modules (Heatmap by folder) ---
    # Group files by the folder they are in (module)
    if files:
        modules = []
        for f in files:
            # take the top-level folder (or the folder the file is in)
            p = Path(f)
            if len(p.parts) > 1:
                modules.append(str(p.parent))
            else:
                modules.append("Root")
        
        module_counts = Counter(modules).most_common(5)
        report.append("  - Most Active Modules/Folders:")
        for mod, count in module_counts:
            report.append(f"    * {mod} ({count} updates)")
    else:
        report.append("  - No activity recorded in this period.")

    # --- 3. TODO / FIXME Scan ---
    # Use git grep to find comments in the code quickly
    # -I = ignore binary files
    # -n = show line numbers
    report.append(f"\nTechnical Debt Scan (TODOs / FIXMEs):")
    
    try:
        # This command will return all lines with TODO or FIXME
        grep_output = run_git_cmd(path, ["grep", "-I", "-n", "-E", "TODO|FIXME"])
        
        if grep_output:
            lines = grep_output.splitlines()
            count = len(lines)
            report.append(f"  Found {count} items. Top critical items:")
            
            # Show only the top 10 to avoid flooding
            for line in lines[:10]:
                # Format is usually: file:line:content
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    fname, linenum, content = parts[0], parts[1], parts[2].strip()
                    # Truncate overly long content
                    if len(content) > 60: content = content[:57] + "..."
                    report.append(f"    [Line {linenum}] {fname}: {content}")
            
            if count > 10:
                report.append(f"    ... and {count - 10} more.")
        else:
            report.append("  Great job! No TODOs or FIXMEs found in the code.")
            
    except Exception:
        report.append("  (Could not scan for TODOs - strictly binary repo or grep error)")

    return "\n".join(report)
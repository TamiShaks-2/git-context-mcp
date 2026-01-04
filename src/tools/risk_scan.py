import os
from pathlib import Path
from collections import Counter
from .git_ops import run_git_cmd

LOC_THRESHOLD = 200
CHURN_THRESHOLD = 5
SKIP_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'dist', 'build'}
SKIP_EXTS = {'.json', '.lock', '.svg', '.png', '.jpg', '.xml', '.map'}

def _count_lines(filepath: Path) -> int:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def get_risk_scan_report(repo_path: str) -> str:
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    report = [f"=== RISK & HEALTH SCAN ===", f"Repo: {path.name}"]
    
    file_stats = {}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in SKIP_EXTS: continue
            loc = _count_lines(file_path)
            if loc > 0:
                rel_path = str(file_path.relative_to(path)).replace('\\', '/')
                file_stats[rel_path] = loc

    churn_counts = Counter()
    changes_raw = run_git_cmd(path, ["log", "-n 50", "--name-only", "--format="])
    if changes_raw:
        for line in changes_raw.splitlines():
            if line.strip(): churn_counts[line.strip()] += 1

    high_risk_files = []
    for fname, loc in file_stats.items():
        churn = churn_counts.get(fname, 0)
        if loc > LOC_THRESHOLD and churn >= CHURN_THRESHOLD:
            high_risk_files.append((fname, loc, churn))

    high_risk_files.sort(key=lambda x: x[1] * x[2], reverse=True)

    if high_risk_files:
        report.append(f"\nCRITICAL HOTSPOTS (High Complexity + High Churn):")
        for fname, loc, churn in high_risk_files[:5]:
            report.append(f"   - {fname} (LOC: {loc}, Changes: {churn})")
    else:
        report.append("\n No critical hotspots detected.")

    return "\n".join(report)
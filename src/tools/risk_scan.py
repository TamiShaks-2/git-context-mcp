import os
from pathlib import Path
from collections import Counter
from .git_ops import run_git_cmd

# סף רגישות (אפשר לשחק עם זה)
LOC_THRESHOLD = 200        # קבצים מעל 200 שורות נחשבים "גדולים"
CHURN_THRESHOLD = 5        # קבצים שהשתנו מעל 5 פעמים לאחרונה

SKIP_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'dist', 'build', 'migrations'}
SKIP_EXTS = {'.json', '.lock', '.svg', '.png', '.jpg', '.xml', '.map'}

def _count_lines(filepath: Path) -> int:
    """Safely counts lines in a file, ignoring binaries."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def get_risk_scan_report(repo_path: str) -> str:
    """
    Performs a risk analysis based on Complexity (LOC), Churn, and Test gaps.
    """
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    report = [f"=== RISK & HEALTH SCAN ===", f"Repo: {path.name}"]
    
    # 1. איסוף נתוני קבצים (Complexity)
    file_stats = {} # {rel_path: loc}
    
    for root, dirs, files in os.walk(path):
        # סינון תיקיות
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in SKIP_EXTS: continue
            
            loc = _count_lines(file_path)
            if loc > 0:
                rel_path = str(file_path.relative_to(path)).replace('\\', '/')
                file_stats[rel_path] = loc

    # 2. איסוף נתוני שינויים (Churn) - 50 קומיטים אחרונים
    churn_counts = Counter()
    changes_raw = run_git_cmd(path, ["log", "-n 50", "--name-only", "--format="])
    
    if changes_raw:
        for line in changes_raw.splitlines():
            clean_line = line.strip()
            if clean_line and clean_line in file_stats:
                churn_counts[clean_line] += 1

    # 3. הצלבת נתונים: High Risk Files
    high_risk_files = []
    large_files = []
    
    for fname, loc in file_stats.items():
        churn = churn_counts.get(fname, 0)
        
        # קובץ גדול + שינויים תכופים = סיכון קריטי
        if loc > LOC_THRESHOLD and churn >= CHURN_THRESHOLD:
            high_risk_files.append((fname, loc, churn))
        
        # סתם קובץ ענק
        elif loc > LOC_THRESHOLD:
            large_files.append((fname, loc))

    # מיון לפי רמת הסיכון (מספר השינויים * גודל)
    high_risk_files.sort(key=lambda x: x[1] * x[2], reverse=True)
    large_files.sort(key=lambda x: x[1], reverse=True)

    # 4. זיהוי חורי בדיקות (Missing Tests)
    # נניח שעל כל תיקייה ב-src צריכה להיות מקבילה ב-tests
    src_dirs = set()
    test_dirs = set()
    
    for f in file_stats.keys():
        parts = f.split('/')
        if 'test' in parts[0] or 'tests' in parts[0]:
            if len(parts) > 1: test_dirs.add(parts[1])
        elif 'src' in parts[0] and len(parts) > 1:
            if len(parts) > 2: src_dirs.add(parts[1]) # src/api/... -> api

    missing_tests = src_dirs - test_dirs

    # --- בניית הדו"ח ---

    # א. Hotspots קריטיים
    if high_risk_files:
        report.append(f"\n🔥 CRITICAL HOTSPOTS (High Complexity + High Churn):")
        report.append(f"   (These files change often AND are large - likely source of bugs)")
        for fname, loc, churn in high_risk_files[:5]:
            report.append(f"   - {fname} (LOC: {loc}, Changes: {churn})")
    else:
        report.append("\n✅ No critical hotspots detected (Architecture looks stable).")

    # ב. סתם קבצים גדולים
    if large_files:
        report.append(f"\n🐘 Large Monoliths (Low Churn, but hard to read):")
        for fname, loc in large_files[:5]:
            report.append(f"   - {fname} ({loc} lines)")

    # ג. כיסוי בדיקות
    report.append(f"\n🛡️ Test Coverage Gaps (Heuristic):")
    if missing_tests:
        report.append(f"   ⚠️ The following 'src' modules seem to miss a matching 'tests' folder:")
        for m in missing_tests:
            report.append(f"      - src/{m} -> tests/{m} (?)")
    else:
        report.append("   ✅ Project structure suggests good test alignment.")

    return "\n".join(report)
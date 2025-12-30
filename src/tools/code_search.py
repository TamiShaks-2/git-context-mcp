from pathlib import Path
from .git_ops import run_git_cmd

def search_code(repo_path: str, query: str, file_pattern: str = "") -> str:
    """
    Fast code search using git grep. Returns matches with context lines.
    """
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    # בניית הפקודה
    # -I: מתעלם מקבצים בינאריים
    # -n: מספרי שורות (חובה לתיקונים)
    # --break --heading: עיצוב נוח לקריאה
    # -C 2: מביא 2 שורות לפני ואחרי (Context)
    cmd = ["grep", "-I", "-n", "--break", "--heading", "-C", "2"]
    
    # חיפוש חכם (Case Insensitive אם אין אותיות גדולות בשאילתה)
    if query.islower():
        cmd.append("-i")
        
    cmd.append(query)
    
    # סינון לפי סוג קובץ (אופציונלי)
    if file_pattern:
        # בגיט גריפ, הסינון הוא בסוף הפקודה עם --
        cmd.append("--")
        cmd.append(file_pattern)

    try:
        output = run_git_cmd(path, cmd)
        
        if not output:
            return f"No matches found for '{query}'."
            
        # יצירת דו"ח קריא
        lines = output.splitlines()
        match_count = output.count(":") # הערכה גסה
        
        # אם יש המון תוצאות, נקצר
        if len(lines) > 300:
            preview = "\n".join(lines[:300])
            return f"Found many matches. Showing top results:\n\n{preview}\n\n... (Output truncated)"
            
        return f"=== SEARCH RESULTS FOR '{query}' ===\n\n{output}"

    except Exception as e:
        return f"Search failed: {str(e)}"
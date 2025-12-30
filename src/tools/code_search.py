from pathlib import Path
from .git_ops import run_git_cmd

def search_code(repo_path: str, query: str, file_pattern: str = "") -> str:
    """
    Fast code search using git grep. Returns matches with context lines.
    """
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    # Build the command
    # -I: ignore binary files
    # -n: show line numbers (useful for fixes)
    # --break --heading: format output for readability
    # -C 2: include 2 lines of context before and after
    cmd = ["grep", "-I", "-n", "--break", "--heading", "-C", "2"]
    
    # Smart search (case-insensitive if the query has no uppercase letters)
    if query.islower():
        cmd.append("-i")
        
    cmd.append(query)
    
    # Filter by file type (optional)
    if file_pattern:
        # In git grep, the file filter is placed after '--'
        cmd.append("--")
        cmd.append(file_pattern)

    try:
        output = run_git_cmd(path, cmd)
        
        if not output:
            return f"No matches found for '{query}'."
            
        # Create a readable report
        lines = output.splitlines()
        match_count = output.count(":") # rough estimate
        
        # If there are many results, truncate the output
        if len(lines) > 300:
            preview = "\n".join(lines[:300])
            return f"Found many matches. Showing top results:\n\n{preview}\n\n... (Output truncated)"
            
        return f"=== SEARCH RESULTS FOR '{query}' ===\n\n{output}"

    except Exception as e:
        return f"Search failed: {str(e)}"
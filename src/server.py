from mcp.server.fastmcp import FastMCP
from tools.git_ops import get_repo_status_report
from tools.git_activity import get_recent_activity_report
from tools.work_summary import get_work_summary
from tools.code_map import get_code_map
from tools.risk_scan import get_risk_scan_report
from tools.code_search import search_code

# Initialize Server
mcp = FastMCP("Dev Context Server")

@mcp.tool()
def project_status(repo_path: str) -> str:
    """
    Returns a technical snapshot of a local git repository.
    Use this to understand the current state of the code, changes, and branch.
    
    Args:
        repo_path: Absolute or relative path to the project root.
    """
    # Delegation to business logic
    return get_repo_status_report(repo_path)

@mcp.tool()
def recent_activity(repo_path: str, n: int = 20) -> str:
    """
    Analyzes recent git history to find 'hot' files and latest changes.
    Use this to understand what happened recently in the project and where the focus is.
    
    Args:
        repo_path: Path to the project root.
        n: Number of commits to analyze (default 20).
    """
    return get_recent_activity_report(repo_path, n)

@mcp.tool()
def work_summary(repo_path: str, since: str = "7d") -> str:
    """
    Summarizes development progress and technical debt.
    
    Args:
        repo_path: Path to the project root.
        since: Time period (e.g., '7d', '2w', '24h'). Default is '7d'.
    """
    return get_work_summary(repo_path, since)

@mcp.tool()
def code_map(repo_path: str, top: int = 25) -> str:
    """
    Generates a file tree and identifies key architectural files (entry points, config).
    Use this to orient yourself in the codebase structure.
    
    Args:
        repo_path: Path to the project root.
        top: Max number of files/folders to display (default 25) to avoid clutter.
    """
    return get_code_map(repo_path, top)

@mcp.tool()
def risk_scan(repo_path: str) -> str:
    """
    Identifies risky areas in the codebase.
    Highlights 'Hotspots' (large files that change often) and potential missing tests.
    Use this to prioritize code reviews or refactoring.
    """
    return get_risk_scan_report(repo_path)

@mcp.tool()
def search_in_code(repo_path: str, query: str, file_pattern: str = "") -> str:
    """
    Searches for a string or pattern in the codebase using git grep.
    Returns the matching lines with surrounding context.
    
    Args:
        repo_path: Path to the project root.
        query: The text to search for (e.g. "def connect_db" or "FIXME").
        file_pattern: Optional filter (e.g. "*.py" or "src/*.js").
    """
    return search_code(repo_path, query, file_pattern)

if __name__ == "__main__":
    mcp.run()
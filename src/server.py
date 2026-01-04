from mcp.server.fastmcp import FastMCP
from tools.project_status import get_repo_status_report
from tools.git_activity import get_recent_activity_report
from tools.work_summary import get_work_summary
from tools.code_map import get_code_map
from tools.risk_scan import get_risk_scan_report

mcp = FastMCP("Dev Context Server")

@mcp.tool()
def project_status(repo_path: str) -> str:
    """Returns a technical snapshot of a local git repository."""
    return get_repo_status_report(repo_path)

@mcp.tool()
def recent_activity(repo_path: str, n: int = 20) -> str:
    """Analyzes recent git history to find 'hot' files."""
    return get_recent_activity_report(repo_path, n)

@mcp.tool()
def work_summary(repo_path: str, since: str = "7d") -> str:
    """Summarizes development progress and technical debt."""
    return get_work_summary(repo_path, since)

@mcp.tool()
def code_map(repo_path: str, top: int = 25) -> str:
    """Generates a file tree and identifies key architectural files."""
    return get_code_map(repo_path, top)

@mcp.tool()
def risk_scan(repo_path: str) -> str:
    """Identifies risky areas (hotspots) in the codebase."""
    return get_risk_scan_report(repo_path)


if __name__ == "__main__":
    mcp.run()

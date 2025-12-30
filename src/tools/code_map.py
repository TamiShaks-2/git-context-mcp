import os
from pathlib import Path
from typing import List, Set

# Directories to ignore to avoid polluting the context
IGNORED_DIRS = {
    '.git', '.venv', 'venv', 'env', '__pycache__', 'node_modules', 
    '.idea', '.vscode', 'dist', 'build', 'coverage'
}

# Patterns to identify important files
ENTRY_POINTS = {
    'main.py', 'app.py', 'server.py', 'wsgi.py', 'manage.py', 'index.js', 
    'server.js', 'go.main', 'Program.cs'
}

CONFIG_FILES = {
    'pyproject.toml', 'requirements.txt', 'package.json', 'Dockerfile', 
    'docker-compose.yml', '.env', 'setup.py', 'cargo.toml', 'go.mod'
}

def _generate_tree(dir_path: Path, prefix: str = "", limit: int = 15, current_count: int = 0) -> tuple[str, int]:
    """Recursive function to build a visual tree string."""
    output = []
    
    # Sorting: directories first, then files
    try:
        items = sorted(os.listdir(dir_path), key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x.lower()))
    except PermissionError:
        return "", current_count

    # Filter items
    filtered_items = [i for i in items if i not in IGNORED_DIRS and not i.startswith('.')]
    
    for i, item in enumerate(filtered_items):
        if current_count >= limit:
            output.append(f"{prefix}... (remaining files truncated)")
            return "\n".join(output), current_count + 1

        is_last = (i == len(filtered_items) - 1)
        connector = "└── " if is_last else "├── "
        full_path = dir_path / item
        
        # Visual markers for important files
        marker = ""
        if item in ENTRY_POINTS: marker = " [🚀 ENTRY POINT]"
        elif item in CONFIG_FILES: marker = " [⚙️ CONFIG]"
        
        output.append(f"{prefix}{connector}{item}{marker}")
        current_count += 1
        
        if full_path.is_dir():
            extension = "    " if is_last else "│   "
            # Recurse into directories (depth implicitly limited by the overall limit)
            sub_tree, new_count = _generate_tree(full_path, prefix + extension, limit, current_count)
            if sub_tree:
                output.append(sub_tree)
            current_count = new_count

    return "\n".join(output), current_count

def get_code_map(repo_path: str, top: int = 25) -> str:
    """
    Generates a concise architectural map of the project.
    Identifies entry points, config files, and directory structure.
    """
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    # 1. Initial scan to find key files in the root
    entry_points_found = []
    config_files_found = []
    
    try:
        root_files = os.listdir(path)
        for f in root_files:
            if f in ENTRY_POINTS: entry_points_found.append(f)
            if f in CONFIG_FILES: config_files_found.append(f)
    except Exception as e:
        return f"Error scanning directory: {str(e)}"

    # 2. Build the tree
    tree_view, _ = _generate_tree(path, limit=top)

    # 3. Build the report
    report = [
        f"=== PROJECT CODE MAP ===",
        f"Root: {path.name}",
        f"Limit: Top {top} files shown",
        ""
    ]

    # Quick summary at the top
    if entry_points_found:
        report.append(f"🚀 Detected Entry Points: {', '.join(entry_points_found)}")
    if config_files_found:
        report.append(f"⚙️ Key Configuration: {', '.join(config_files_found)}")
    
    report.append("\nDirectory Structure:")
    report.append(tree_view)
    
    return "\n".join(report)
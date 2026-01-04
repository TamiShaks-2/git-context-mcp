import os
from pathlib import Path

IGNORED_DIRS = {
    '.git', '.venv', 'venv', 'env', '__pycache__', 'node_modules', 
    '.idea', '.vscode', 'dist', 'build', 'coverage'
}

ENTRY_POINTS = {
    'main.py', 'app.py', 'server.py', 'wsgi.py', 'manage.py', 'index.js', 
    'server.js', 'go.main', 'Program.cs'
}

CONFIG_FILES = {
    'pyproject.toml', 'requirements.txt', 'package.json', 'Dockerfile', 
    'docker-compose.yml', '.env', 'setup.py', 'cargo.toml', 'go.mod'
}

def _generate_tree(dir_path: Path, prefix: str = "", limit: int = 15, current_count: int = 0) -> tuple[str, int]:
    output = []
    try:
        items = sorted(os.listdir(dir_path), key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x.lower()))
    except PermissionError:
        return "", current_count

    filtered_items = [i for i in items if i not in IGNORED_DIRS and not i.startswith('.')]
    
    for i, item in enumerate(filtered_items):
        if current_count >= limit:
            output.append(f"{prefix}... (remaining files truncated)")
            return "\n".join(output), current_count + 1

        is_last = (i == len(filtered_items) - 1)
        connector = "└── " if is_last else "├── "
        full_path = dir_path / item
        
        marker = ""
        if item in ENTRY_POINTS: marker = " [ENTRY POINT]"
        elif item in CONFIG_FILES: marker = " [CONFIG]"
        
        output.append(f"{prefix}{connector}{item}{marker}")
        current_count += 1
        
        if full_path.is_dir():
            extension = "    " if is_last else "│   "
            sub_tree, new_count = _generate_tree(full_path, prefix + extension, limit, current_count)
            if sub_tree:
                output.append(sub_tree)
            current_count = new_count

    return "\n".join(output), current_count

def get_code_map(repo_path: str, top: int = 25) -> str:
    path = Path(repo_path).resolve()
    if not path.exists():
        return f"ERROR: Path '{path}' does not exist."

    tree_view, _ = _generate_tree(path, limit=top)
    
    report = [
        f"=== PROJECT CODE MAP ===",
        f"Root: {path.name}",
        "\nDirectory Structure:",
        tree_view
    ]
    return "\n".join(report)
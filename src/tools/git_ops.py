import subprocess
import os
import sys
from pathlib import Path
from typing import List, Optional

def run_git_cmd(cwd: Path, args: List[str]) -> str:
    """
    Executes a git command safely and returns stdout.
    Handles environment setup and error catching.
    """
    # Environment settings to avoid hangs on Windows (no pagers, no prompts)
    env = os.environ.copy()
    env["GIT_PAGER"] = "cat"
    env["GIT_TERMINAL_PROMPT"] = "0"

    try:
        # stdin=subprocess.DEVNULL prevents the process from waiting for user input
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            stdin=subprocess.DEVNULL,
            env=env
        )
        
        # CRITICAL FIX: Ensure stdout is not None before stripping
        if result.stdout is None:
            return ""
            
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Specific handling for 'git grep':
        # Exit code 1 means "no matches found", which is NOT an error for us.
        if "grep" in args and e.returncode == 1:
            return ""
            
        # For other git errors, return empty to keep server alive
        sys.stderr.write(f"!!!critical Git Executi Error: {e}\n")
        return ""
        
    except Exception as e:
        sys.stderr.write(f"!!! Critical Python Error: {e}\n")
        return ""
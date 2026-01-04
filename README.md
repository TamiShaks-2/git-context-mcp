# git-context-mcp

A **local Model Context Protocol (MCP) server** that provides structured, high-signal insight into a Git repository, enabling AI coding agents to understand **project state, structure, activity, and risk** — without uploading or modifying the codebase.

> **Note**  
> This README was generated using `git-context-mcp` itself, by connecting an AI assistant to the repository through the exposed MCP tools.

---

## Problem This Project Solves

AI coding agents (Claude Code, Cursor, Codex, Gemini, etc.) are powerful, but they lack **situational awareness** when working with non-trivial codebases.

They often struggle to answer questions like:
- What is the current state of this project?
- Where are the real entry points?
- What parts of the code are actively changing?
- Which files are risky to touch?

`git-context-mcp` solves this by turning **Git history and repository structure** into **explicit, machine-readable context** that AI agents can consume before writing or reviewing code.

---

## What This MCP Does (and Does Not)

### What it does
- Runs locally as a standalone MCP process
- Reads only Git metadata and repository files
- Exposes read-only analysis tools
- Works over STDIO (compatible with MCP Inspector and desktop coding agents)
- Provides high-level context, not raw source dumps

### What it does not do
- Does not modify the repository
- Does not upload code anywhere
- Does not execute project code
- Does not depend on external services or APIs

---

## Overview

`git-context-mcp` is a **local-first MCP server** focused on **development context extraction**, not repository manipulation.

It exposes Git-based analysis tools that help AI coding agents quickly understand:
- Repository structure and entry points
- Current working state and sync status
- Recent development activity and churn
- Technical debt indicators (TODO / FIXME)
- Files with elevated maintenance or bug risk

---

## Typical Usage Flow

1. **project_status** – understand branch, cleanliness, and sync state  
2. **code_map** – locate entry points and important modules  
3. **recent_activity** – identify active or volatile areas  
4. **work_summary** – understand recent work and open debt  
5. **risk_scan** – flag risky files before editing  

---

## Features

### project_status
Snapshot of the current Git repository state.

### code_map
Structured directory tree with identification of important files.

### recent_activity
Analysis of Git history to surface frequently modified files.

### work_summary
High-level summary of recent development and technical debt.

### risk_scan
Detection of large, complex, or high-churn files.

---

## Requirements

- Python 3.10+
- Git installed and available on PATH
- A local Git repository to analyze

---

## Installation

```bash
git clone https://github.com/TamiShaks-2/git-context-mcp.git
cd git-context-mcp

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# or
.venv\Scripts\activate    # Windows

pip install -e .
```

---

## Running with MCP Inspector

Transport Type: STDIO  

Command:
```
<path-to-venv>/python
```

Arguments:
```
src/server.py
```

---

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| project_status | Repository state awareness |
| code_map | Structural understanding |
| recent_activity | Development churn analysis |
| work_summary | High-level progress overview |
| risk_scan | Maintenance risk detection |

All tools operate in read-only mode.

---

## Project Structure

```
git-context-mcp/
├── src/
│   ├── tools/
│   │   ├── code_map.py
│   │   ├── git_activity.py
│   │   ├── git_ops.py
│   │   ├── project_status.py
│   │   ├── risk_scan.py
│   │   └── work_summary.py
│   └── server.py
├── tests/
├── pyproject.toml
└── README.md
```

---

## Testing

```bash
pytest
```

---

## License

MIT License

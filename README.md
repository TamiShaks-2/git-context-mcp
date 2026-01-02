# git-context-mcp

A Model Context Protocol (MCP) server that provides deep, structured insight into a local Git repository, enabling AI coding agents to understand project state, structure, activity, and risk — without uploading the full codebase.

> **Note**  
> This README was generated using this MCP server itself, by connecting it to an AI assistant and analyzing the repository through the exposed MCP tools.

---

## Overview

`git-context-mcp` is a local MCP server designed for development context awareness.

It exposes Git-based analysis tools that help developers and AI coding agents (such as Claude) quickly understand:

- Repository structure and entry points  
- Recent development activity  
- Technical debt indicators  
- High-risk or high-churn areas in the codebase  

The server runs locally and communicates over **STDIO**, making it fully compatible with **MCP Inspector** and desktop AI coding agents.

---

## Features

### Repository Analysis Tools

- **Project Status**  
  Snapshot of the current repository state (branch, uncommitted changes, sync status).

- **Code Map**  
  Directory tree visualization with identification of key and entry-point files.

- **Recent Activity**  
  Analysis of Git history to surface frequently modified (“hot”) files.

- **Work Summary**  
  High-level summary of recent development and scan for technical debt (TODOs / FIXMEs).

- **Risk Scan**  
  Detection of complex or high-churn files that may represent higher maintenance or bug risk.

---

## Requirements

- Python 3.10+  
- Git installed and available on the command line  
- A local Git repository to analyze  

---

## Installation

```bash
git clone <repository-url>
cd git-context-mcp

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# or
.venv\Scripts\activate    # Windows

pip install -e .
```

---

## Running with MCP Inspector

This project is designed to work with the official **MCP Inspector**.

### Inspector Configuration

- **Transport Type**: STDIO  
- **Command**: Path to the Python executable inside the virtual environment  
- **Arguments**:
  ```
  src/server.py
  ```

### Example (Windows)

```
Command:
C:\Path\To\git-context-mcp\.venv\Scripts\python.exe

Arguments:
src/server.py
```

**Important**:  
Do not copy absolute paths from examples. Always use the Python executable from your own virtual environment.

---

## Available Tools

### project_status
Returns the current Git repository state.

**Parameters**
- repo_path (string)

---

### code_map
Generates a directory structure and highlights important files.

**Parameters**
- repo_path (string)  
- top (integer, optional, default: 25)

---

### recent_activity
Analyzes recent Git commits and file churn.

**Parameters**
- repo_path (string)  
- n (integer, optional, default: 20)

---

### work_summary
Summarizes recent development progress and scans for technical debt.

**Parameters**
- repo_path (string)  
- since (string, optional, default: "7d")

---

### risk_scan
Identifies potentially risky areas in the codebase.

**Parameters**
- repo_path (string)

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

## Use Cases

- Providing repository context to AI coding agents  
- Accelerating onboarding to unfamiliar codebases  
- Identifying technical debt and risky files  
- Supporting AI-assisted code review and planning  

---

## License

MIT License

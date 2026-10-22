# Pynst Command Syntax Reference

This document outlines the standard `.pynst.txt` command vocabulary, parameters, and CLI options supported by CrossOS Pynst.

## Core Commands Reference

### Environment & Repositories

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `PYTHON` | `version` | Sets Python version required for the environment. | `PYTHON 3.13` |
| `SETVENV` | `relative_dir` | Ensures virtual environment exists at path (relative to target). If `requirements.txt` is in the folder, installs it automatically. | `SETVENV .` |
| `CLONEIT` | `url target_dir [name]` | Clones a git repository into `target_dir` (or optional subfolder `name`). If already cloned, updates it. | `CLONEIT https://github.com/a/b ComfyUI/custom_nodes` |
| `CLONELF` | `url target_dir [name]` | Clones repository and deletes `.git` history to save disk space (blob clone). Supports smart caching. | `CLONELF https://github.com/a/b ComfyUI/custom_nodes` |

### Dependency & Package Management

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `REQFILE` | `url_or_path` | Installs pip packages from a local file or remote HTTP/HTTPS URL into the active venv. | `REQFILE requirements.txt` |
| `REQFILEFORCE` | `url_or_path` | Same as `REQFILE`, but forces reinstallation of all packages (`--force-reinstall`). | `REQFILEFORCE requirements.txt` |
| `REQSCAN` | `relative_dir` | Scans directory 1 level deep for subdirectories containing `requirements.txt`. Pulls latest git updates and installs requirements. | `REQSCAN ComfyUI/custom_nodes` |
| `PIPINST` | `args...` | Passes arguments directly to `pip install` in the active venv. | `PIPINST torch torchvision` |
| `RFILTER` | `pkg1 [pkg2 ...]` | Filters specified packages from being installed by subsequent `REQ*` commands. Call with no arguments to clear all filters. | `RFILTER torch torchvision` |

### Direct Execution & Sub-installers

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `DOPYNST` | `[options] file_or_url target_dir` | Calls another `.pynst.txt` installer (local path or remote HTTP/HTTPS URL) with standard pynst arguments and executes it. | `DOPYNST other.pynst.txt target/` |
| `XRUNPYTHONFILE` | `script args...` | Executes a Python file immediately in the active venv. | `XRUNPYTHONFILE setup.py --init` |
| `XRUNCMD_GIT` | `relative_cwd args...` | Executes a raw `git` command in the specified directory. | `XRUNCMD_GIT ComfyUI checkout dev` |
| `XRUNCMD_PIP` | `args...` | Executes a raw `pip` command directly in the active venv. | `XRUNCMD_PIP freeze` |

### File & Asset Operations

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `GETFILE` | `url target_dir` | Downloads a file if missing or if file size differs. Supports smart local caching. | `GETFILE http://example.com/file.txt target/` |
| `GETBLOB` | `url target_dir` | Downloads large binary/model files. Can be skipped via the `--noblob` CLI flag. Supports smart local caching. | `GETBLOB https://huggingface.co/model.safetensors ComfyUI/models/checkpoints` |
| `HASFILE` | `relative_path` | Confirms that a required file exists; aborts execution if missing. | `HASFILE ComfyUI/main.py` |

### Shortcuts & Launchers

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `DESKICO` | `label script args...` | Creates a clickable Desktop Shortcut (`.lnk` on Windows, `.app` bundle on macOS). | `DESKICO "ComfyUI" main.py --cpu` |
| `DESKEXE` | `label script args...` | Creates a Desktop launch script (`.bat` on Windows, `.sh` on Linux/macOS). | `DESKEXE "Launch Comfy" main.py` |
| `HOMEICO` | `label script args...` | Creates a clickable shortcut inside the installation directory. | `HOMEICO "ComfyUI" main.py` |
| `HOMEEXE` | `label script args...` | Creates a launch script (`.bat` or `.sh`) inside the installation directory. | `HOMEEXE "Launch Comfy" main.py` |

### Flow Control & Logging

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `PRINTIT` | `message` | Prints an informational message to the console. | `PRINTIT Loading custom nodes...` |
| `PAUSEIT` | none | Pauses execution and waits for user confirmation (press Enter). | `PAUSEIT` |
| `#` | any | Comment line prefix. Ignored during execution. | `# This is a comment` |

---

## Supported CLI Flags

Pynst CLI flags can be passed on the command line or used inside `DOPYNST` calls:

| Flag | Description |
| :--- | :--- |
| `--update` | Updates all packages installed from requirement files to the newest allowed version. |
| `--upgrade` | Force upgrade or reinstall of packages installed by requirement files. |
| `--revenv` | Deletes/empties the virtual environment and rebuilds it from scratch. |
| `--senso` | Conservative mode. Only adds missing components; does not pull or update existing repositories. |
| `--embedded` | Treats installation as portable using a `python_embedded` folder. |
| `--gitlatest` | Forces git repositories to the absolute newest commit on the main/master branch. |
| `--safecheck` | Validates that existing components exist before modifying (prevents accidental duplicate installs). |
| `--backup` | Backs up existing venv (renaming to `.bak`) before rebuilding. |
| `--venvname <name>` | Specifies a custom virtual environment directory name. |
| `--noblob` | Skips all `GETBLOB` commands to save bandwidth. |
| `--nodesktop` | Disables creation of desktop shortcuts. |
| `--dryrun` | Simulates execution without modifying the filesystem. |
| `--verbose` | Displays full output from subprocesses (pip, git). |

---

## Example Templates

### 1. General Application Template

```pynst
PYTHON 3.10
CLONEIT https://github.com/loscrossos/core_rope .
SETVENV .
GETFILE https://github.com/Hillobar/Rope/releases/download/Sapphire/det_10g.onnx core_rope/models
DESKICO "Core Rope" core_rope/Rope.py
```

### 2. Composed / Modular Application (Using DOPYNST)

```pynst
# First run base ComfyUI installer
DOPYNST installers/comfy_installer_rtx_full.pynst.txt .

# Then install additional custom nodes & models
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes
REQSCAN ComfyUI/custom_nodes
GETBLOB https://huggingface.co/Phr00t/WAN2.2-14B-Rapid-AllInOne/resolve/main/wan2.2-i2v-rapid-aio-example.json ComfyUI/user/workflows
```

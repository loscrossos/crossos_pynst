# CrossOS Pynst Manual

**CrossOS Pynst** is a single-file, cross-platform (Windows, Linux, macOS) tool designed to automate the installation, management, and repair of Python projects. It reads a simple plain-text instruction file (`.pynst.txt`) and executes it to set up environments, download files, clone repositories, and create shortcuts.

## Table of Contents

1. [Installation](#installation)
2. [Basic Concepts](#basic-concepts)
3. [CLI Usage](#cli-usage)
4. [Instruction File Reference](#instruction-file-reference)
5. [Advanced Features](#advanced-features)
   - [Embedded Python Mode](#embedded-python-mode)
   - [Repair & Rebuild](#repair--rebuild)
   - [Package Filtering](#package-filtering)
   - [Multiple Venvs](#multiple-venvs)
6. [Troubleshooting](#troubleshooting)

---

## Installation

Pynst requires no installation. It is a single Python script.

1.  **Prerequisites**:
    *   **Python 3.8+**: Must be installed and available in your system `PATH`.
    *   **Git**: Must be installed and available in your system `PATH`.
    
    > **Tip:** If you are new to this or setting up a fresh machine, use [**CrossOS Setup**](https://github.com/loscrossos/crossos_setup). It's a free, open-source tool that automatically installs Python, Git, and other necessary libraries for you on Windows, Linux, or macOS.

2.  **Get Pynst**:
    Download `pynst.py` and place it anywhere (e.g., in your project root or a utilities folder).

---

## Basic Concepts

Pynst operates on three main components:

1.  **The Installer File (`.pynst.txt`)**: A text file containing a list of commands (like `CLONEIT`, `REQFILE`, `DESKICO`) that describe the desired state of the installation.
2.  **The Target Directory**: The base folder where Pynst will install everything (repositories, virtual environments, downloaded files).
3.  **The Virtual Environment (Venv)**: Pynst automatically manages Python virtual environments within the target directory to keep dependencies isolated.

---

## CLI Usage

Run Pynst from your terminal:

```bash
python pynst.py [OPTIONS] <input_file> <target_directory>
```

### Examples

**Standard Install:**
```bash
python pynst.py installers/my_app.pynst.txt ./my_app_install
```

**Repair / Rebuild Venv:**
```bash
python pynst.py installers/my_app.pynst.txt ./my_app_install --revenv
```

**Portable/Embedded Install:**
```bash
python pynst.py installers/my_app.pynst.txt ./portable_app --embedded
```

### Options

| Option | Description |
| :--- | :--- |
| `--update` | **update**: updates all existing libraries to the newest and shinniest. |
| `--upgrade` | **force upgrade**: Force upgrade or reinstall of libraries installed by req files(stronger than update, will do a reinstall even if version is the same). |
| `--revenv` | **Rebuild Venv**: Deletes (or empties) the existing virtual environment and rebuilds it from scratch. Essential for fixing broken environments. |
| `--senso` | **Senso Mode**: "Sensitive/Conservative" installation. Only adds missing plugins/files. Does NOT update code (`git pull`) or remove existing files. Safe for updates where you don't want to touch the core. |
| `--embedded` | **Embedded Mode**: Treats the installation as a portable one using a `python_embedded` folder instead of a standard system venv. |
| `--gitlatest` | **Force Latest Git**: Forces all git repositories to the absolute latest commit on `main`/`master`, even if they are in a detached HEAD state. |
| `--safecheck` | **Safety Check**: Verify that major components (Git repos, key files) already exist before proceeding. Useful to ensure you are updating an existing install and not accidentally creating a new one or overwriting the wrong folder. |
| `--backup` | **Backup**: Backs up the existing virtual environment (renames it with a `.bak` suffix) before making changes. |
| `--venvname <name>` | **Custom Venv Name**: Use a specific name for the virtual environment folder (e.g., `venv_gpu`, `venv_cpu`) instead of the default `.env_{os}`. |
| `--noblob` | **No Blobs**: Skips commands marked as `GETBLOB`. Useful for updating code/dependencies without downloading massive model files again. |
| `--nodesktop` | **No Desktop Shortcuts**: Prevents creation of desktop icons, even if the installer file requests them. |
| `--dryrun` | **Dry Run**: Simulates the execution without changing any files. Prints what would happen. |
| `--verbose` | **Verbose**: Shows full output from subprocesses (pip, git) for debugging. |

---

## Instruction File Reference

The `.pynst.txt` file is read line-by-line. Lines starting with `#` are comments.

### Core Commands

#### `PYTHON <version>`
Asserts that the system has a specific Python version available. If `--embedded` is used, checks the embedded python version.
```bash
PYTHON 3.10
```

#### `CLONEIT <url> <path>`
Clones a Git repository into `[TargetDir]/[path]/[RepoName]`.
*   If the repo exists, it updates it (unless `--senso` is used).
*   If `--gitlatest` is used, it forces a checkout of the latest main/master branch.
```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
# Result: [TargetDir]/ComfyUI
```

#### `SETVENV <path>`
Ensures a virtual environment exists at `[TargetDir]/[path]`.
*   If `requirements.txt` exists at that path, it is automatically installed.
*   Default names: `.env_win` (Windows), `.env_lin` (Linux), `.env_mac` (macOS).
```bash
SETVENV ComfyUI
```

#### `REQFILE <path_or_url>`
Installs a requirements file into the current venv using `pip`. Can be a local path (relative to TargetDir) or a remote URL.
```bash
REQFILE ComfyUI/requirements.txt
REQFILE https://example.com/extra_requirements.txt
```

#### `REQFILEFORCE <path_or_url>`
Same as `REQFILE` but forces re-installation of packages (`--force-reinstall`).

#### `PIPINST <package_list>`
Runs `pip install` directly with the provided arguments.
```bash
PIPINST numpy pandas
PIPINST torch --index-url https://download.pytorch.org/whl/cu118
```

#### `RFILTER <word1> <word2> ...`
Sets a **global filter** for requirements files. Any line in a `REQFILE` starting with these words will be ignored.
*   Useful for preventing conflicts (e.g., filtering `torch` to install a specific version later).
*   Case-insensitive. Matches the start of the package name.
*   Call without arguments to clear the filter.
```bash
RFILTER torch torchvision  # Ignore standard torch/torchvision
REQFILE requirements.txt   # install everything EXCEPT torch/torchvision
RFILTER                    # Clear filter
```

#### `REQSCAN <path>`
Scans **one level deep** inside `[TargetDir]/[path]` for subdirectories containing `requirements.txt`.
*   If a subdirectory is a Git repo, it attempts to `git pull` first.
*   Then it installs the found `requirements.txt`.
*   **Ideal for plugins/custom nodes.**
```bash
REQSCAN ComfyUI/custom_nodes
```

### File Operations

#### `GETFILE <url> <path_suffix>`
Downloads a file to `[TargetDir]/[path_suffix]`.
*   Only downloads if the file is missing or the server file size differs.
```bash
GETFILE https://example.com/workflow.json ComfyUI/user/workflows
```

#### `GETBLOB <url> <path_suffix>`
Same as `GETFILE`, but intended for large binary files (models, weights).
*   Can be skipped by the user with the `--noblob` CLI flag.
```bash
GETBLOB https://huggingface.co/model.safetensors ComfyUI/models/checkpoints
```

#### `HASFILE <path>`
Verifies that `[TargetDir]/[path]` exists. Aborts if missing.
*   Used for safety checks to ensure the installation structure is valid before proceeding.
```bash
HASFILE ComfyUI/main.py
```

### Shortcuts & Execution

#### `DESKICO <Label> <Script> <Args...>`
Creates a clickable **Desktop Shortcut** (Icon) that runs a command using the installed venv.
*   **Label**: Name of the shortcut (quoted if spaces).
*   **Script**: Python script path relative to TargetDir.
*   **Args**: Arguments for the script.
```bash
DESKICO "ComfyUI GPU" ComfyUI/main.py --gpu
```
*(Also available: `DESKEXE` (script file), `HOMEICO` (icon in install dir), `HOMEEXE` (script in install dir))*

#### `XRUNPYTHONFILE <Script> <Args...>`
Runs a Python script immediately using the venv.
```bash
XRUNPYTHONFILE setup_db.py --init
```

#### `XRUNCMD_GIT <Dir> <Args...>`
Runs a raw `git` command in the specified directory (relative to TargetDir).
```bash
XRUNCMD_GIT ComfyUI checkout dev_branch
```

#### `XRUNCMD_PIP <Args...>`
Runs a raw `pip` command.
```bash
XRUNCMD_PIP uninstall -y torch
```

### Utility

#### `PRINTIT <Message...>`
Prints a message to the console.
```bash
PRINTIT "Downloading massive models, please wait..."
```

#### `PAUSEIT`
Pauses execution and waits for user confirmation (Enter).

---

## Advanced Features

### Embedded Python Mode
Use `--embedded` to manage portable installations (like ComfyUI Portable).
*   Pynst looks for a folder named `python_embedded` (or `python_embeded`) in the target directory.
*   It uses the Python executable inside that folder.
*   `--revenv` in this mode will **empty** the site-packages of the embedded python instead of deleting the folder.

### Package Filtering
The `RFILTER` command is powerful for managing conflicting dependencies, especially with AI libraries like PyTorch.
1.  **Filter**: `RFILTER torch`
2.  **Install**: `REQFILE requirements.txt` (skips torch)
3.  **Manual Install**: `PIPINST torch==2.1.0+cu121 ...` (installs correct version)
4.  **Clear**: `RFILTER`

### Multiple Venvs
You can maintain multiple environments for the same project using `--venvname`.
1.  Install default: `python pynst.py install.txt ./app` (Creates `.env_win`)
2.  Install CPU version: `python pynst.py install.txt ./app --venvname venv_cpu` (Creates `venv_cpu`)
3.  The `DESKICO` commands generated will be linked to the specific venv active during that run.

### Repair & Rebuild
*   **Repair**: Running Pynst on an existing directory updates repos and installs missing requirements.
*   **Rebuild**: Adding `--revenv` nukes the venv and starts fresh. This is the "Turn it off and on again" for Python environments.

### Cross-Platform Icons
Pynst generates platform-native icons with text labels generated on the fly:
*   **Windows**: `.lnk` shortcuts with `.ico` icons.
*   **macOS**: `.app` bundles with `.icns` icons.
*   **Linux**: `.desktop` entries with `.png` icons.

# CrossOS Pynst: Iron-Clad Python Installation Manager

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** single-file Python tool that installs, rebuilds, updates, upgrades, extends and repairs virtually any Python project with a single command.  

Whether you want to **install from scratch**, **repair an existing environment**, or **fully re-harden** a complex multi-repo setup like ComfyUI, WAN2GP, or a custom AI pipeline-Pynst automates the heavy lifting while keeping your existing code and data safe.

Pynst sets up the virtual environment, clones and updates repositories, installs requirements, downloads files, creates launcher shortcuts and much more!

---

## Overview

CrossOS Pynst manages:

- Python versions and virtual environments (venv or embedded)
- Git repositories and plugin modules
- Requirement files (local or remote)
- Desktop shortcuts and launcher scripts
- Safe rebuilds and full-environment repairs 
- File downloads

You can run it directly with:

```bash
python pynst.py [pynst-installer-file] [targetdirectory] [optional commands]
```

No installation, no dependencies, no platform issues.

---

## Features

- Easy to Use
  - Just download `pynst.py` and run it. All you need is an PIF (pynst-installer-file) and a target directory.
  - The pif defines what to install. It is a plain-text instruction file. Use one of the provided examples, check out the community or write one yourself! Everything else is automated.
- Fully Cross-OS
  - Works identically on **Windows**, **Linux**, and **macOS**. Learn once use forever!
  - Dual/multi-boot friendly: projects you install can be used across all OSes. Access the same installation from Windows, Linux and MacOS!
- Powerful Installation
  - Installs and configures full projects in one step.
  - Automatically installs the right files on the right place
  - Creates desktop or home-directory launchers automatically.
- Repair & Rebuild
  - Rebuilds or repairs broken or outdated venvs. ComfyUI broke? just repair it!
  - Works on embedded/portable installs.
  - Ensures correct Python and dependency versions. No more dependency jungle.
- Safety & Clarity
  - Colorized logging and clear status messages.
  - Dry-run mode for safe testing.
  - Backup mode for risk-free environment replacement.

---

## Quick Start

Simple example to install ComfyUI and load a full fledgew Workflow into it.

### Pre-requisites

You need git and python installed to run pynst. Pynst uses by default python 3.13 (it can be changed)

**Windows**

if you havent already installed them, open an administrator console and run these commands:

```
winget install --id=Python.Python.3.13 -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Git.Git -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
```

### 1. ComfyUI simple installation

A `.inst.txt` file defines what to install and how. Example for the simplest install of comfyUI.

Save this as `test.comfyhelloworld.inst.txt` or use the provided example in the `installers` folder:

```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
DESKICO "ComfyUI CPU" ComfyUI/main.py --cpu
```

Then run (example on windows):
```bash
python pynst.py installers/test.comfyhelloworld.inst.txt ./hellocomfy
```

This will: 

1. clone the comfyUI repository under the target directory `hellocomfy/ComfyUI`
2. automatically create a virtual environment `hellocomfy/ComfyUI/.env_win` (example on windows) while searching and installing the requirements it finds in the ComfyUI directory.
3. create a starter icon on the desktop.

Just double-click the starter icon! thats it. You have a ComfyUI installed with latest code.


### 2. Load a full fledged workflow into ComfyUI with ALL dependencies!

Now lets upgrade ComfyUI to load a workflow.








---

## Command-Line Options

```
usage: pynst.py [-h] [--revenv] [--senso] [--embedded] [--nodesktop]
                        [--dryrun] [--verbose] [--backup] [--noblob]
                        [--venvname VENVNAME] [--gitlatest]
                        [--safecheck] 
                        inputfile targetdirectory
```

**mandatory arguments**

| Argument | Description |
|-----------|--------------|
| `inputfile` | Path to instruction file (`.pynst.txt`) |
| `targetdirectory` | Target base directory for installation or repair |

**Options**

| Option | Description |
|---------|--------------|
| `--revenv` | Rebuild the venv from zero; deletes the old venv and rebuilds one correctly. In embedded mode it fixes broken environments removing all packages and reinstalling them correctly. |
| `--embedded` | Treat installation as portable "python_embedded" install. |
| `--nodesktop` | Skip creation of desktop shortcuts. |
| `--dryrun` | Simulated run: no changes, just prints intended actions (including system commands). |
| `--verbose` | Show full subprocess output for debugging. |
| `--backup` | Backup existing venv before deleting/replacing or changing anything (backup is the original name and a suffix on the same location). |
| `--noblob` | Skip optional large file downloads (e.g., model blobs). |
| `--venvname` | Provide a custom virtual-environment folder name. |
| `--gitlatest` | Force git repository code to the newest version on the main/master branch (sometimes called 'nightly') |
| `--safecheck` | Check to see if  we update existing installations. This option performs a pre-Check AND only proceeds if: a) repositories (marked by CLONEIT) to be cloned already exist AND b) marked required files (by HASFILE) exist. This helps ensure an installation will be updated and the target exists. Else a typo would cause a full installation in parallel to an existing one. |
| `--senso` | Ultra Safe mode: avoids overwriting or deleting existing code (only for special cases. do not use this unless you know what you are doing). |
| `--debugtest` | Output debug info and exit. |

---

## Example Use Cases

**Install ComfyUI**
```bash
python pynst.py comfy_install.pynst.txt /ai/comfy
```

**Repair an existing install by rebuilding the virtual environment**
```bash
python pynst.py comfy_install.pynst.txt /ai/comfy --revenv
```

**Update without downloading model blobs**
```bash
python pynst.py visomaster.pynst.txt /ai/visomaster --noblob
```

**Force nightly git updates**
```bash
python pynst.py comfy.pynst.txt /ai/comfy --gitlatest
```

---

## Instruction File Format

Each `.pynst.txt` file is a list of **commands**, executed sequentially.

```
[COMMAND] [PARAMETER1] [PARAMETER2] ...
```

Comments start with `#` and are ignored.



---

## Command Reference

| Command | Parameters | Description |
|----------|-------------|--------------|
| **PYTHON** | version | Use a specific Python version (e.g. `3.12`). Aborts if unavailable. |
| **SETVENV** | path | Ensures a venv exists under this relative path. Creates it if missing. If a 'requirements.txt' is found in the path, then it is installed.|
| **REQFILE** | file / URL | Installs a requirements file into the current venv (local or remote). Packages installed with this command have priority over files installed with 'SETENV' or 'REQSCAN' (force-reinstall-mode). |
| **PIPINST** | package list | Passes arguments directly to `pip install`. installs wheels or modules to the current venv. Can be wheel file URL (not a file path) or a pip package or several packages |
| **RFILTER** | word list | Filters out matching packages from requirement installs. Case-insensitive; “torch” does not match “torchaudio”. |
| **CLONEIT** | URL path | Clones a git repository into `[target]/[path]`. Installs its `requirements.txt` if present. |
| **REQSCAN** | path | Scans one directory level under `[target]/[path]` for `requirements.txt` files and installs them. |
| **GETFILE** | URL | Downloads a file if missing or size differs. |
| **GETBLOB** | URL | Same as GETFILE but optional; skipped if `--noblob` used. |
| **HASFILE** | path | Verifies that a file exists; aborts otherwise. |
| **PRINTIT** | text | Prints a custom message for the user. |
| **PAUSEIT** | - | Pauses execution until user confirms. |
| **DESKICO**, **HOMEICO** | label + command | Creates an OS-specific shortcut icon (desktop or install directory). |
| **DESKEXE**, **HOMEEXE** | label + command | Creates a `.bat` or `.sh` launcher script. |
| **XRUNGITCOMMAND** | git args | Passes raw commands directly to git. |
| **XRUNPIPCOMMAND** | pip args | Passes raw commands directly to pip. Advanced use only. |
| **XRUNPYTHONFILE** | script args | Runs a Python file directly through the venv interpreter. |
| **#** | none | Comment line. Lines beginning with `#` are ignored. |

---

## Virtual-Environment Rules

- Default Python version: **3.13**, unless changed by `PYTHON`.
- Venvs are created under the target directory:
  - `.env_win` (Windows)
  - `.env_lin` (Linux)
  - `.env_mac` (macOS)
- Embedded mode uses `python_embedded/python.exe` or equivalent.
- In `--backup` mode, an existing venv is renamed with `.bak`.
- In repair mode, corrupted entries and stale `~` folders are removed before rebuilding.

---

## Technical Notes

CrossOS Pynst is designed to be **completely self-contained**:

- Uses **only Python standard libraries** (no third-party dependencies).
- Compatible with Python ≥ 3.8 on Windows, Linux, and macOS.
- Relies solely on 2 tools (`python`, `git`).
- Fully path-safe: works with spaces and Unicode paths.
- All subprocess calls are encapsulated for cross-OS consistency.
- Default output is colorized using ANSI sequences on all supported shells.

Internally, the script:
1. Parses instruction files line-by-line.
2. Validates the environment and Python version.
3. Creates or repairs virtual environments.
4. Executes commands in sequence, respecting filters and safe modes.
5. Provides rollback (backup) when applicable.

---
 

## Summary

CrossOS Pynst is your **universal Python project installer and fixer** -  
a single file that safely automates everything from scratch setups to delicate venv repairs, across any platform.

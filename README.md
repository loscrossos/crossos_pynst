# CrossOS Pynst: Iron-Clad Python Installation Manager

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** single-file Python project manager that installs, rebuilds, updates, upgrades, extends and repairs virtually any Python project with a single command.  

Whether you want to **install from scratch**, **repair an existing environment**, or **fully enhance** a complex multi-repo setup like ComfyUI, WAN2GP, or a custom AI pipeline - Pynst automates the heavy lifting while keeping your existing code and data safe.

No complex obscure formats: It uses a simple plain text file with instruction commands and executes them to create the ultimate installation. Its so simple you can create your own recipes!


##  Documentation
- **[Reference Manual](doc/MANUAL.md)**: Complete command reference, CLI options, and advanced usage.
- **[ComfyUI Tutorial](doc/tutorial_comfy.md)**: A guide to installing a fully accelerated ComfyUI environment.

---

##  Quick Start

No installation required. Just download `pynst.py`.

### 1. Simple Example

Save this as `install.pynst.txt`:
```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV .
DESKICO "ComfyUI" main.py
```

Run it:
```bash
python pynst.py install.pynst.txt ./my_comfy_install
```
This will clone the repo, create a virtual environment, install requirements, and put a shortcut on your desktop (no matter your OS!).

### 2. Common Commands

**Install / Update:**
The same pynst file can be used to update your installation! just run it again:
```bash
python pynst.py my_installer.txt ./target_dir
```

**Repair (Rebuild Venv):**
```bash
python pynst.py my_installer.txt ./target_dir --revenv
```

**Safe Update (Don't touch code):**
```bash
python pynst.py my_installer.txt ./target_dir --senso
```

---

##  Key Features

- **Iron-clad Environments**: Automatically builds isolated virtual environments (`venvs`). Can repair or rebuild them with a single flag `--revenv`.
- **Truly Cross-Platform**: Works identically on **Windows**, **Linux**, and **macOS**. Install on a USB drive and run it anywhere.
- **Smart Dependency Management**: 
  - **`REQSCAN`**: Recursively finds and installs `requirements.txt` from all sub-repositories (great for plugins).
  - **`RFILTER`**: Global package filtering to prevent dependency hell (e.g., exclude `torch` to install a specific version later).
- **Instant Shortcuts**: Generates native desktop icons and launcher scripts automatically on all OSes: Windows, Linux, macOS.
- **Embedded/Portable Support**: Fully supports managing "Portable" Python installations (like ComfyUI Portable) using the `--embedded` flag.
- **Safe & Secure**: 
  - **`--senso` mode**: Updates plugins/files without touching core code.
  - **`--backup` mode**: Backs up your environment before touching it.
  - **`--safecheck`**: Verifies integrity before running.

---

## Command Summary

| Command | Description |
| :--- | :--- |
| `CLONEIT <url> <path>` | Clone/Update a git repo. |
| `SETVENV <path>` | Create/Use a virtual environment. |
| `REQFILE <path>` | Install a requirements file. |
| `REQSCAN <path>` | Recursively find and install requirements from subdirs. |
| `GETFILE <url>` | Download a file. |
| `RFILTER <pkgs>` | Filter out specific packages. |
| `DESKICO <label> <cmd>` | Create a desktop shortcut. |

*(See the [Manual](doc/MANUAL.md) for the full list)*
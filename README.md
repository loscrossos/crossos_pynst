# CrossOS Pynst: Iron-Clad Python Installation Manager

**Stop writing installation manuals. Start writing installation code.**

**One file. All platforms. Any Python project.**

CrossOS Pynst is a **cross-platform (Windows, Linux, macOS)** single-file Python project manager. It automates the entire lifecycle of a Python application: installation, updates, repairs, and extensions.

From simple scripts to complex AI pipelines like ComfyUI or WAN2GP, Pynst handles the heavy lifting—cloning repos, building venvs, installing dependencies, and creating desktop shortcuts—with a single command.

## ⚡ Why Pynst?

### The "Sweet Spot" of Installation
Pynst bridges the gap between fragile manual instructions and heavy containerization.

| Method | Reproducible? | Cross-Platform? | Native Performance? | Easy to Read? |
| :--- | :---: | :---: | :---: | :---: |
| **Manual Clicking** | ❌ | ❌ | ✅ | ✅ |
| **Bash / Batch Scripts** | ❌ | ❌ | ✅ | ❌ |
| **Docker** | ✅ | ✅ | ❌ (overhead) | ❌ |
| **CrossOS Pynst** | ✅ | ✅ | ✅ | ✅ |

### Key Features
*   **🦄 Single File, Zero Dependencies**: No `pip install` required. Just `python pynst.py`.
*   **🛡️ Indestructible Environments**: Breaks happen. Use `--revenv` to nuke and rebuild the virtual environment instantly. It's "Have you tried turning it off and on again?" for your Python setup.
*   **🌍 Write Once, Run Anywhere**: The same instruction file works on Windows, Linux, and macOS.
*   **🚀 Native Desktop Integration**: Automatically generates clickable **Desktop Icons** (`.lnk`, `.app`, `.desktop`) for your scripts.
*   **📦 Smart Dependency Management**:
    *   **`REQSCAN`**: Recursively finds and installs `requirements.txt` from all sub-folders (perfect for plugin systems).
    *   **`RFILTER`**: Global package filtering to solve dependency hell (e.g., "install everything *except* Torch").
*   **💾 Portable/Embedded Mode**: fully supports "Portable" installations (like ComfyUI Portable). Can even convert a portable install into a full system install.

---

## 🚀 Quick Start

### 1. The "Hello World" Example
Save this as `install.pynst.txt`:

```bash
# Clone the repo
CLONEIT https://github.com/comfyanonymous/ComfyUI .

# Create the venv & install requirements
SETVENV .

# Create a desktop shortcut
DESKICO "ComfyUI" main.py
```

### 2. Run It
```bash
python pynst.py install.pynst.txt ./my_app
```
**Done.** You now have a fully installed application with a desktop icon.

---

## 🛠️ Common Operations

**Update an Installation**
Run the same file again. Pynst updates code and installs new requirements automatically.
```bash
python pynst.py install.pynst.txt ./my_app
```

**Repair a Broken Venv**
Something weird happening? Rebuild the environment from scratch.
```bash
python pynst.py install.pynst.txt ./my_app --revenv
```

**Safe Update ("Senso" Mode)**
Update plugins and files *without* touching the core code.
```bash
python pynst.py install.pynst.txt ./my_app --senso
```

---

## 📚 Documentation

*   **[Reference Manual](doc/MANUAL.md)**: Full command list, CLI options, and advanced usage.
*   **[ComfyUI Tutorial](doc/tutorial_comfy.md)**: Step-by-step guide to installing a fully accelerated ComfyUI environment.

---

## 🧩 Command Summary

| Command | Description |
| :--- | :--- |
| `CLONEIT <url> <path>` | Clone or update a git repository. |
| `SETVENV <path>` | Ensure a virtual environment exists (and install its requirements). |
| `REQFILE <path/url>` | Install a requirements file (local or remote). |
| `REQSCAN <path>` | Recursively find and install `requirements.txt` in subdirectories. |
| `GETFILE <url> <path>` | Download a file (smart check for existing files). |
| `DESKICO <label> <cmd>` | Create a clickable desktop shortcut. |
| `RFILTER <pkgs>` | Filter out specific packages to avoid conflicts. |

*(See the [Manual](doc/MANUAL.md) for the full list)*

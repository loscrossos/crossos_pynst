---
name: pynst-generator
description: Generates or updates crossos-pynst installer configuration files (.pynst.txt) from source texts, links, or ComfyUI workflow JSON files. Use when asked to write or modify Pynst install scripts for workflows, setups, or applications.
---

# Pynst Installer Script Generator

This skill guides the creation and maintenance of CrossOS-Pynst installer configuration files (`.pynst.txt`). Pynst recipes automate dependency installation, environment setup, model downloads, and launcher shortcut creation across Windows, Linux, and macOS.

## Authoring Guidelines & Syntax Rules

- **Command Casing:** Command keywords must ALWAYS be UPPERCASE (e.g., `CLONEIT`, `SETVENV`, `PYNSTIT`, `REQSCAN`).
- **Path Semantics:** Target directory paths in commands are relative to the installation root directory (`in_basedir`), unless using `PYNSTIT` which accepts CLI paths relative to the current working directory or web URLs.
- **Quoting:** Always wrap parameters containing spaces in double quotes (e.g., `DESKICO "ComfyUI GPU" ComfyUI/main.py --gpu`).
- **Comments & Blank Lines:** Lines starting with `#` are comments. Blank lines are ignored.

---

## Workflow Scenarios

### 1. ComfyUI Workflow Recipes (Addons & Nodes)
When generating a `.pynst.txt` recipe for a ComfyUI workflow:
- **Do NOT re-install ComfyUI itself.** Assume ComfyUI and its base virtual environment exist at the root.
- **Custom Nodes:**
  - Parse non-standard node types from the workflow JSON.
  - Map each node to its Git repository URL.
  - Add `CLONEIT <git_url> ComfyUI/custom_nodes`.
- **Dependencies:**
  - Always add `REQSCAN ComfyUI/custom_nodes` to install requirements from all cloned custom nodes.
- **Model Downloads:**
  - Map model names to their proper destination under `ComfyUI/models/<category>` (e.g., `checkpoints`, `unet`, `loras`, `vae`, `clip`).
  - Always use `GETBLOB <url> ComfyUI/models/<category>` for model weights so users can skip large downloads via `--noblob`.
  - See [references/comfyui-mapping.md](references/comfyui-mapping.md) for standard folder mappings and node repositories.

### 2. Standalone General Applications
When creating a full installer for a Python tool or project:
- **Python Version:** Declare `PYTHON <version>` (e.g., `PYTHON 3.10` or `PYTHON 3.13`).
- **Clone Code:** Clone the main repository using `CLONEIT <url> .` (or specific subfolder).
- **Environment:** Initialize the virtual environment using `SETVENV <dir>`. If a `requirements.txt` is in `<dir>`, it installs automatically.
- **Hardware Accelerators / PyTorch:**
  - If a specific PyTorch/CUDA build is required, install it first via `REQFILE <url_or_path>` or `PIPINST`.
  - Use `RFILTER torch torchvision torchaudio` before `REQSCAN` or secondary `REQFILE` calls to prevent dependencies from overwriting the accelerated PyTorch wheel. Clear filters with `RFILTER` once done.
- **Large Assets:** Use `GETBLOB <url> <path>` for weights/models and `GETFILE <url> <path>` for configs.
- **Shortcuts & Launchers:**
  - `DESKICO <label> <script> <args...>` for desktop application icon.
  - `HOMEEXE <label> <script> <args...>` for local launch script in the install directory.

### 3. Modular & Composed Applications (`PYNSTIT`)
When composing recipes or building on top of base installations:
- Use `PYNSTIT [options] <file_or_url> <target_dir>` to execute another `.pynst.txt` recipe.
- Can invoke local recipe files (e.g., `PYNSTIT installers/comfy_installer_rtx_full.pynst.txt .`) or remote URLs (e.g., `PYNSTIT https://example.com/base.pynst.txt ./target`).
- Supports standard Pynst CLI flags (e.g., `--embedded`, `--noblob`, `--revenv`).

### 4. Advanced System Calls & Validation
- **Integrity Validation:** Use `HASFILE <path>` to verify critical files exist before proceeding.
- **Direct Python Invocation:** Use `XRUNPYTHONFILE <script> <args...>` to run one-off initialization scripts within the active venv.
- **Direct Git Commands:** Use `XRUNCMD_GIT <relative_dir> <args...>` for checking out specific branches, tags, or running submodules.
- **Direct Pip Commands:** Use `XRUNCMD_PIP <args...>` for raw pip flags (e.g. `--extra-index-url`, `freeze`).

---

## Quick Reference Links

- **Full Command & Flag Reference:** See [references/pynst-commands.md](references/pynst-commands.md)
- **ComfyUI Mappings & Nodes:** See [references/comfyui-mapping.md](references/comfyui-mapping.md)

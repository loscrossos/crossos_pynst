# Pynst Command Syntax Reference

This document outlines the standard `.pynst.txt` command vocabulary and parameters.

## Core Commands

| Command | Arguments | Description | Example |
| :--- | :--- | :--- | :--- |
| `PYTHON` | `version` | Sets Python version to be used for venvs. | `PYTHON 3.13` |
| `SETVENV` | `relative_dir` | Ensures virtual env exists at path (relative to target). | `SETVENV .` |
| `CLONEIT` | `url target_dir [name]` | Clones a git repo. | `CLONEIT https://github.com/a/b ComfyUI/custom_nodes` |
| `CLONELF` | `url target_dir [name]` | Clones git repo and deletes `.git` history (blob-clone). | `CLONELF https://github.com/a/b ComfyUI/custom_nodes` |
| `REQFILE` | `url_or_path` | Installs pip packages from requirements file to current venv. | `REQFILE requirements.txt` |
| `REQSCAN` | `relative_dir` | Scans directory for subdirectories containing requirements.txt and installs them. | `REQSCAN ComfyUI/custom_nodes` |
| `PIPINST` | `args` | Passes args directly to `pip install`. | `PIPINST torch torchvision` |
| `RFILTER` | `pkg1 pkg2 ...` | Filters specified packages from being installed by subsequent `REQ*` commands. | `RFILTER torch` |
| `GETFILE` | `url target_dir` | Downloads a file if it doesn't exist or size is different. | `GETFILE http://example.com/file.txt target/` |
| `GETBLOB` | `url target_dir` | Used for large model files (can be skipped via `--noblob` flag). | `GETBLOB https://huggingface.co/model.safetensors ComfyUI/models/checkpoints` |
| `HASFILE` | `relative_path` | Aborts execution if target file does not exist. | `HASFILE ComfyUI/main.py` |
| `PRINTIT` | `message` | Prints informational message to output terminal. | `PRINTIT Loading custom nodes...` |
| `PAUSEIT` | none | Pauses execution and waits for user confirmation. | `PAUSEIT` |
| `DESKICO` | `name script args` | Creates desktop shortcut. | `DESKICO "Comfy" main.py --cpu` |
| `HOMEEXE` | `name script args` | Creates workspace launcher script. | `HOMEEXE "Launch Comfy" main.py` |
| `#` | any | Comment prefix. Ignored during execution. | `# This is a comment` |

## Template for Independent General Application

```pynst
PYTHON 3.10
CLONEIT https://github.com/loscrossos/core_rope .
SETVENV .
GETFILE https://github.com/Hillobar/Rope/releases/download/Sapphire/det_10g.onnx core_rope/models
DESKICO "Core Rope" core_rope/Rope.py
```

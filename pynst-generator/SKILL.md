---
name: pynst-generator
description: Generates or updates crossos-pynst installer configuration files (.pynst.txt) from source texts, links, or ComfyUI workflow JSON files. Use when asked to write or modify Pynst install scripts for workflows, setups, or applications.
---

# Pynst Installer Script Generator

This skill guides the creation of CrossOS-Pynst installer configuration files (`.pynst.txt`) based on raw source text containing download links or ComfyUI workflow JSON files.

## Workflow Overview

To write a `.pynst.txt` file:
1. **Analyze the Source:** Determine if the input is a plain text list of links, a structured document, or a ComfyUI workflow JSON.
2. **For ComfyUI Workflows:**
   - **Do NOT install ComfyUI itself.** Assume a base installation of ComfyUI exists at the root.
   - Parse node types (excluding built-in ComfyUI nodes) to identify required custom nodes.
   - Map custom nodes to their Git repository URLs and add `CLONEIT <git_url> ComfyUI/custom_nodes` commands.
   - Parse workflow model names (checkpoints, LoRAs, VAEs, ControlNets, upscalers, etc.).
   - Find public URLs (e.g., Hugging Face, Civitai) for those models and add `GETBLOB <url> ComfyUI/models/<category>` commands.
   - Run a `REQSCAN ComfyUI/custom_nodes` to automatically install custom node dependencies.
3. **For General Applications:**
   - Define Python version, venv location, git cloning, and download commands.
   - Reference [references/pynst-commands.md](references/pynst-commands.md) for command syntax.
   - Reference [references/comfyui-mapping.md](references/comfyui-mapping.md) for ComfyUI custom node and model folder mappings.

## Quick Reference Links

- **Pynst Syntax & Commands:** See [references/pynst-commands.md](references/pynst-commands.md)
- **ComfyUI Mappings & Nodes:** See [references/comfyui-mapping.md](references/comfyui-mapping.md)

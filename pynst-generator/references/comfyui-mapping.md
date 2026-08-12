# ComfyUI Directory & Node Mapping Guide

When translating ComfyUI workflows into `.pynst.txt` installers:

## Model Categories & Destination Folders

Map the files referenced in workflow load nodes to their standard ComfyUI folders:

| Filename Suffix / Node Type | ComfyUI Model Destination Folder | Category |
| :--- | :--- | :--- |
| `.safetensors` (Load Checkpoint / UNET) | `ComfyUI/models/checkpoints` | Checkpoint / Base Model |
| `.safetensors` (Load LoRA) | `ComfyUI/models/loras` | LoRA |
| `.safetensors` / `.pt` (Load VAE) | `ComfyUI/models/vae` | VAE |
| `.pth` / `.onnx` (ControlNet) | `ComfyUI/models/controlnet` | ControlNet |
| `.pth` / `.onnx` (Upscale Model / ESRGAN) | `ComfyUI/models/upscale_models` | Upscaler |
| `.onnx` / `.pth` (InsightFace / FaceSwap) | `ComfyUI/models/insightface` | Face Models |
| `.safetensors` / `.bin` (IP-Adapter) | `ComfyUI/models/ipadapter` | IP-Adapter |
| `.safetensors` / `.bin` (Text Encoder / CLIP) | `ComfyUI/models/clip` | CLIP / T5 |
| `.safetensors` / `.pt` (AnimateDiff Motion) | `ComfyUI/models/animatediff_models` or `ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models` | Motion Module |

*Use `GETBLOB` for downloading any of these files into their specified folders.*

## Mapping Common Node Types to Repositories

If a node `"type"` is not built-in, clone its host custom node repository under `ComfyUI/custom_nodes`:

| Node `"type"` Sample | Host Repository URL | Target Directory |
| :--- | :--- | :--- |
| `ReActorFaceSwap` | `https://github.com/Gourieff/comfyui-reactor-node.git` | `ComfyUI/custom_nodes` |
| `KJNodes...` | `https://github.com/kijai/ComfyUI-KJNodes.git` | `ComfyUI/custom_nodes` |
| `AnimateDiff...` | `https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git` | `ComfyUI/custom_nodes` |
| `IPAdapter...` | `https://github.com/cubiq/ComfyUI_IPAdapter_plus.git` | `ComfyUI/custom_nodes` |
| `ControlNetLoader...` | `ComfyUI` (Built-in) | N/A |
| `UltimateSDUpscale` | `https://github.com/Coyote-A/ultimate-upscale-for-comfyui.git` | `ComfyUI/custom_nodes` |
| `WanVideo...` | `https://github.com/kijai/ComfyUI-WanVideoWrapper.git` | `ComfyUI/custom_nodes` |

## ComfyUI Workflow Installer Standard Template

For a workflow-based installer, ComfyUI itself and its venv are assumed to be pre-installed. The configuration should look like this:

```pynst
# Custom Nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

# Automatically install custom nodes requirements
REQSCAN ComfyUI/custom_nodes

# Required Models
GETBLOB https://huggingface.co/Kijai/WanVideo_ComfyUI/resolve/main/wan2.1_i2v_480p_14B_quantized.safetensors ComfyUI/models/unet
GETBLOB https://huggingface.co/comfyanonymous/wan_2.1_text_encoder_and_vae_gguf/resolve/main/umt5_xxl_fp8_e4m3fn.safetensors ComfyUI/models/clip
```

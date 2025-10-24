# Pynst Tutorial - Install the perfect ComfyUI

**Linux/MacOS:** All Examples use a windows path `d:\temp\mytestcomfy`. For linux or Macos the command is exactly the same. just use a unix path e.g. `/User/Shared/mycomfy`.

### Overview

Pynst is a powerful tool to securely install, manage and repair your comfyUI setup. It also can fully install workflows (the workflow file AND the models and the right dependencies).
This all depends on an installer file (which is a plain text file with instructions). The definition file can be provided by someone or you can easily define one yourself!

Here we will define such a file. If all you want is to install ComfyUI, then you dont need the tutorial. The full file is in the repo in the folder `installers/comfy_installer_rtx_full.pynst.txt`. 
Also because of that, you dont have to remember or note the example. Just sit back and relax.


In this tutorial we will learn how to build a perfect ComfyUI installation file that can be used with Pynst. It will be a full fledged ComfyUI installation with the latest code, all accelerators installed, some of the best plugins pre-installed and setup and some nice icons on the desktop to just click and start! then we will see how we can use it to manage a new installation or your existing installation. This way you can build your own or expand an existing file to your liking. Therefore this tutorial is more to learn how pynst works.

To use an installation file all you need to run is:

```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt [your target directory]
```

for example on Windows:

```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt d:\temp\mytestcomfy
```

This command does the folowing:
- it calls python (the version is not important as pynst is not version dependent as long as its python 3.xx+)
- it instructs to use the `pynst.py` file
- the **first parameter is which pynstaller to use**: we use `pynstallers/comfy_installer_rtx_full.pynst.txt`
- the **second parameter is the target directory**: where the project will be installed: e.g. on windows `d:\temp\mytestcomfy`

**IMPORTANT**

The "target directory": pynst installs always in a directory that contains all files and repositories. So here the target project directory would be `mytestcomfy` and all files that pynst creates will be placed under it (cloned repos, images, icons): e.g. if this pynstaller clones comfyUI, then comfy will be placed under it: `d:\temp\mytestcomfy\ComfyUI`

Normally all paths within a pynstaller file will be relative to the target dir.


### Pre-requisites

On an OS level, you should have git and python installed. 

In general i heartedly advice to setup your PC with my automatic AI-Setup installer. Its free open source and fully setups your Windows, Mac or Linux PC with all needed libraries and dependencies you will ever need for AI projects.

https://github.com/loscrossos/crossos_setup

to get the minumal possible requirements you can also do this.

**Windows**

On Windows you should also have Visual C Redistributable installed

open an administrator console and enter these commands to install git, python and VC Redistributable from official sources.
```
winget install --id=Python.Python.3.13 -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Git.Git -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
winget install --id=Microsoft.VCRedist.2015+.x64 -e  --silent --accept-package-agreements --accept-source-agreements --scope machine
```

**MacOS**

use brew to install git and python3.13



## Lets define a full fledged accelerated ComfyUI

Lets build a pynstaller that installs a brand new ComfyUI preloaded with accelerators and plugins!

### Installing a Repo

The most basic setup to run a repository is usually to clone a repository (e.g. from github) and to create a virtual environment.
With Pynst this is done with 2 commands:

```bash
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
```

The commands:
- the first command (`CLONEIT`) instructs to clone the comfyUI repository to the target directory (represented by a dot "." ). If there is already a repository at that location then the command updates its code to the latest version (`git pull`)
- the second command `SETVENV` ensures a venv is under the directory `ComfyUI`. why "ensures"?: if there is already a venv there then it will be used. if not one will be created.

**VENV name:** by default pynst names a venv depending on the OS: on windows `.env_win`, on linux `.env_lin` and on mac `.env_mac`. This way you can install a project on a shared drive and access it from different OSes and it will work on all of them.

**VENV Creation**: you can place a VENV anywhere you want. It does not really matter. To keep things ordered it is good practice to put it under the directory of the repository it belongs to. If you have several repos that share a venv you can put it under the target directory by setting the parameter as a dot "."

**Automatic requirements installation**: `SETENV` searches the directory where the venv is placed and if it finds a `requirements.txt` it automatically installs it.

So after running this two commands as indicated at the beginning we would have this structure:

```
|-mytestcomfy
    |-ComfyUI
        |-.env_win
        |-requirements.txt
        |-main.py
        |-(other comfyUIfiles)
        |-(other files)
```

At this point we have a ready-to-use comfyUI installation: ComfyUI was cloned, a venv was created and the requirements.txt was installed into the venv. We could start comfy by activating the venv and running the `main.py` file
```bash
.env_win\Scripts\activate
python main.py
```

but now is where it starts to get interesting....


### Securing the installation

We add a check that the repository was correctly installed by checking the existence of the `ComfyUI/main.py` file. This check also ensures that running in `--safecheck` later will abort if the file is not found. This way an update only works if the correct path has been given.


### Installing extra files

ComfyUI comes by default with no accelerators installed. To add them, one must activate the venv and install a requirements file. For this we will use the command `REQINST` (REQuirements INSTallation) which takes an URL as a parameter. We use it to install the accelerator file from my [Crossos Acceleritor project](https://github.com/loscrossos/crossOS_acceleritor). This file is compatible with Python 3.12 and 3.13.

Since we use a file that needs Python 3.13 we use the definer `PYTHON` at the beginning to ensure the whole installation is based on python 3.13. This also ensures that if a user uses the pynstaller to try to install on an existing installation with a different python version, then Pynst will abort warning that the target is incompatible.

Then we add a simple text warning with `PRINTIT`, telling the user that this step might take some time.. else the user might think the process is stuck:


```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt

```


### Adding more repositories at custom locations

ComfyUI accepts plugins: those are simply repositories cloned under the subdirectory `ComfyUI/custom_nodes`

so we use the `CLONEIT` command with some repositories that we like. Just put as many as you want with the target `ComfyUI/custom_nodes` and pynst will clone them.


For a complete installation we need to install their `requirements.txt` into the main venv. This is done with `REQSCAN`: this command accepts as parameter a directory that is scanned for subdirectories that are repositories, for each repository found it will update their code (`git pull`) and install the requirements file from it (if there is one present) into the last venv defined by `SETVENV`. `REQSCAN` will search for ANY repository under its defined target: therefore it will also update and install existing directories (plugins).

```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt


CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

REQSCAN ComfyUI/custom_nodes
```

### Adding Starter icons

so.. how do we start it? normally you would have to open a command line, activate the venv and start the python file `main.py`.

With pynst we can define some neat starter icons to appear right on your desktop! or if you prefer old style start files (`bat` files on windows, `sh` files on Mac/Lin).

just define the `DESKICO`, `DESKEXE` for desktop or`HOMEEXE` and `HOMEICO` for the target directory location, add a label to be used and the start command which is appended to the venvs python. 

For example: to start ComfyUI in awy that uses the GPU, enables Sage Attention and auto-starts the browser when Comfy is loaded, you would need a command that that uses the current virtual environments Python and starts the file `main.py` (located under the `ComfyUI` folder, located in your installation directory) and uses the options `--gpu --use-sage-attention --auto-launch`. Therefore you would normally have this command line:

```
[path to your venv]/python [installdir]/ComfyUI/main.py --gpu --use-sage-attention --auto-launch
````

With Pynst we are going to define such an starter icon on your Desktop called "ComfyUI GPU Mode". We only need the label, and the starter file and options. Pynst automatically uses the last venv defined by `SETVENV`

```
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
```

The `DESKICO` uses as label the first word (several words in quotes count as one word) and everything after that as the starter command. To make a starter icon in the home directory just use `HOMEICO`. To make it a starter file (bat or sh) just replace `ICO` wiht `EXE`.

Here is the finished file!

```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt


CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

REQSCAN ComfyUI/custom_nodes
HOMEEXE "ComfyUI_cpu" ComfyUI/main.py --cpu --auto-launch 
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
DESKICO "ComfyUI CPU Mode" ComfyUI/main.py --cpu  --auto-launch 
```

so now we have a full fledged ComfyUI installation:
- ComfyUI installed
- A virtual environment (venv) automatically created and setup
- Accelerators installed
- as many plugins installed as you want
- All code updated to latest version
- Starter Icons on the Desktop in several versions

Mind you this works on Windows, Mac and Linux!









## Managing your ComfyUI installation

Now that we defined how the installation looks like now, lets learn how to manage it!

We are going to use a windows path for the scenarios, but these commands work the same on Linux or MacOS.

One thing that is important to understand is that pynsts target directory is the base. Anyting it installs will be under it:

If you put the target directory as `mytestcomfy` then the ComfyUI repo and all target paths are placed under it:

```
|-mytestcomfy
    |-ComfyUI
        |-.env_win
        |-requirements.txt
        |-main.py
        |-(other comfyUIfiles)
        |-(other files)
```

If you want to repair a Comfy instance that is in `C:\temp\ComfyUI`, then you have to use `c:\temp`as target directory

### Install ComfyUI

install comfyui on any path you like (you can have 10, 20 installations or as many as you want in parallel), all of them with all the accelerators in the latest versions preinstalled and enabled. As seen above this also installs startable icons on your desktop.

```bash
python pynst.py pynstallers/comfy_installer_rtx_full.pynst.txt [your target directory]
```


### Install any plugins your want

install comfy with plugins: add any plugins that you want and have it preinstalled. Just add any amount of entries to the section where the plugins are.
The format is:
```
CLONEIT [Gitub URL] [custom nodes path on comfy]
# example:
CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
```

For example:


```bash
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
HASFILE ComfyUI/main.py
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_torch280cu129_lite.txt

# add plugins here
CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

REQSCAN ComfyUI/custom_nodes
HOMEEXE "ComfyUI_cpu" ComfyUI/main.py --cpu --auto-launch 
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
DESKICO "ComfyUI CPU Mode" ComfyUI/main.py --cpu  --auto-launch 
```



### Repair an existing installation

If your installation is "broken", the most likely culprit is a broken virtual environment (a.k.a "venv"). Pynst can fully rebuild your venv by adding the option `--revenv`. Then it will delete the venv it encounters and rebuild it from scratch using the definition found in the installer. If you have an embedded python installation use additionally the option `--embedded`: it then does not delete the venv but empties it, repairs errors (removing broken packages) and reinstalls all packages.
The default name is `.env_mac`, `.env_win` or `.env_lin` depending on OS.
By using the file from the first half the venv will be fully rebuilt and accelerators will be installed.


## Add starter Dekstop Icons to your existing installation

If all you want are some nice starter icons, you can get them with a minimal file. 
This way you can simply add desktop icons to your existing installation to just have a nice clickable starter on your desktop for any configuration you want! One for ComfyCPU one for ComfyGPU, one for ComfyGPU with Sageattention or one for each installation of comfy on your PC

- For this we check that the `main.py` file exists under `[targetDir]/ComfyUI`.
- then we create two starter icons: one for GPU mode called "ComfyUI GPU Mode" and one for CPU.

this example is provided in the file `comfy_only_deskicons.pynst.txt`
```
HASFILE ComfyUI/main.py
DESKICO "ComfyUI GPU Mode" ComfyUI/main.py --gpu --use-sage-attention --auto-launch 
DESKICO "ComfyUI CPU Mode" ComfyUI/main.py --cpu  --auto-launch 
```



### Safely install a full ComfyUI workflow (models and plugins included)

Installing a workflow is not only installing the json file.

- you need several models in the right folders
- you often need additional plugins.

The plugin "Comfy manager" can often load missing plugins. For models you often get text instructions "put model xxx in folder yy".... yet still you have to know what to install. Wouldnt it be great if one file would install everything? yes. EVERYTHING!!

Enter pynst!

Someone sharing a model can define everything to be downloaded and pynst takes care to do the installation.

Safely and securely install any workflow (including models and plugins): have your favorite workflow installed and all models automatically downloaded to the right place! Pynst takes care that its fully fail safe! You can not do anything wrong!

On the installers folder there are several examples of full models to checkout.

This example from the file `installers/comfy_wflow_qwen_edit.pynst.txt` will:

- download a json file to the `ComfyUI/user/default/workflows` folder so its automatically available when you open the "workflows" menu item in comfy
- download models to the correct folders `ComfyUI/models/unet`, `loras`, `text_encoders` and `vae`. If the model is already there it does not load it again.. great!
- install the GGUF loading plugin (only if its not already installed!) and install it in comfy.


```
GETFILE https://raw.githubusercontent.com/loscrossos/comfy_workflows/refs/heads/main/comfy_wf_qwen_edit_safetensorGGUF.json                 ComfyUI/user/default/workflows

GETFILE https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main/Qwen_Image_Edit-Q6_K.gguf                                       ComfyUI/models/unet
GETFILE https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Lightning-8steps-V1.1.safetensors                      ComfyUI/models/loras
GETFILE https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors    ComfyUI/models/text_encoders
GETFILE https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors  	                    ComfyUI/models/vae

CLONEIT https://github.com/city96/ComfyUI-GGUF                                                                                              ComfyUI/custom_nodes
 
REQSCAN                                                                                                                                     ComfyUI/custom_nodes
```

So basically run the file and everything is fully setup and ready.. no more desperately looking for missing models.



### Update your portable ComfyUI to the latest bleeding edge version

So.. you installed the embedded version: you have a "comfyUI portable" installation... but turns out that portable is out of date? Easily and safely convert it to a bleeding edge manual installation with the latest code and all accelerators!

just add the option `--gitlatest` to your installation.. like so:


```bash
python pynst.py installers/comfy_installer_rtx_full.pynst.txt d:\temp\mytestcomfy --gitlatest
```

This option will force all repositories it finds to be set to the latest version.

### Convert your embedded installation to a manual installation

TODO


### Install multiple venvs to a single ComfyUI installation

install as many venvs as you want in parallel for one single Comfy installation and have separate starter icons on your desktop!
-one with sageattention (SA)
-one without SA
-one with python 3.12 or  3.13 or 3.8
-one only for nunchaku wokrflows




 Wait. you are still reading?? Are you not sold yet? I would be long ago!


### Senso-Install


-SensoInstall mode: this mode will not update code or remove anything. It only intalls plugins and files in the safest and most conservative way possible (special case. You do want latest code!).

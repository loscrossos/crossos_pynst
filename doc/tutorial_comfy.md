# Pynst Tutorial - Install the perfect ComfyUI

In this tutorial we will learn how to build a perfect ComfyUI installatation with Pynst and how the Pynstaller definition file is built. This way you can build your own or expand an existing file to your liking. Therefore this tutorial is more to learn how pynst works.

If all you want is to install ComfyUI, then you dont need the tutorial. The full pynst file is in the repo in the folder `pynstallers`. 

all you need to run is:

```bash
python crossos_pynst.py pynstallers/comfyui_installer_nvidia_accelerated.pynst.txt d:\temp\mytestcomfy
```

This command does the folowing:
- it calls python (the version is not important as pynst is not version dependent as long as its python 3.xx+)
- it instructs to use the `crossos_pynst.py` file
- the **first parameter is which pynstaller to use**: we use `pynstallers/comfyui_installer_nvidia_accelerated.pynst.txt`
- the **second parameter is the target directory**: where the project will be installed: e.g. on windows `d:\temp\mytestcomfy`

The "target directory": pynst installs always in a directory that contains all files and repositories. So here the target project directory would be `mytestcomfy` and all files that pynst creates will be placed under it (cloned repos, images, icons): e.g. if this pynstaller clones comfyUI, then comfy will be placed under it: `d:\temp\mytestcomfy\ComfyUI`

Normally all paths within a pynstaller file will be relative to the target dir.


## Basic Installation

Lets build a pynstaller that installs a brand new ComfyUI!



### Installing a Repo



The most basic setup to run a repository is usually to clone a repository (e.g. from github) and to create a virtual environment.
With Pynst this is done with 2 commands:

```
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
mytestcomfy
    |-ComfyUI
        |-.env_win
        |-(other comfyUIfiles)
        |-(other files)
```

At this point we have a ready-to-use comfyUI installation: ComfyUI was cloned, a venv was created and the requirements.txt was installed into the venv.


### Installing extra files

ComfyUI comes by default with no accelerators installed. to add them one must activate the venv and install a requirements file. For this we will use the command `REQINST` (REQuirements INSTallation) which takes an URL as a parameter. We use it to install the accelerator file from my other project [Crossos_Acceleritor](https://github.com/loscrossos/crossOS_acceleritor). 

Since we use a file that needs Python 3.13 we use the definer `PYTHON` at the beginning to ensure the whole installation is based on python 3.13. This also ensures that if a user uses the pynstaller to try to install on an existing installation with a different python version, then Pynst will abort warning that the target is incompatible.

Then we add a simple text warning with `PRINTIT`, telling the user that this step might take some time.. else the user might think the process is stuck:


```
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_python313torch280cu129_lite.txt

```


### Adding more repositories at custom locations

ComfyUI accepts plugins: those are simply repositories cloned under the subdirectory `ComfyUI/custom_nodes`

so we use the `CLONEIT` command with some repositories that we like. Just put as many as you want with the target `ComfyUI/custom_nodes` and pynst will clone them.


For a complete installation we need to install their `requirements.txt` into the main venv. This is done with `REQSCAN`: this command accepts as parameter a directory that is scanned for subdirectories that are repositories, for each repository found it will update their code (`git pull`) and install the requirements file from it (if there is one present) into the last venv defined by `SETVENV`. `REQSCAN` will search for ANY repository under its defined target: therefore it will also update and install existing directories (plugins).


```
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_python313torch280cu129_lite.txt


CLONEIT https://github.com/ltdrdata/ComfyUI-Manager ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-KJNodes ComfyUI/custom_nodes
CLONEIT https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet ComfyUI/custom_nodes
CLONEIT https://github.com/kijai/ComfyUI-WanVideoWrapper ComfyUI/custom_nodes
CLONEIT https://github.com/city96/ComfyUI-GGUF ComfyUI/custom_nodes

REQSCAN ComfyUI/custom_nodes
```

### Adding Starter icons


so.. how do we start it? normally you would have to open a command line, activate the venv and start the python file `main.py`.

With pynst we can define some neat starter icons right on your desktop! or if you prefer old style start files.

just define the `DESKICO`, `DESKEXE` for desktop or`HOMEEXE` and `HOMEICO` for the target directory location, add a label to be used and the start command which is appended to the venvs python. 

Voila the finished file!

```
PYTHON 3.13
CLONEIT https://github.com/comfyanonymous/ComfyUI .
SETVENV ComfyUI
PRINTIT This step may take some time depending on your connection.
REQINST https://raw.githubusercontent.com/loscrossos/crossOS_acceleritor/refs/heads/main/acceleritor_python313torch280cu129_lite.txt


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
- ComfyUI and as many plugins installed as you want
- All code updated to latest version
- Virtual environment created and all plugins installed into it
- Accelerators installed
- Starter Icons on the Desktop

Mind you this works on Windows, Mac and Linux!

## Use Case Scenarios

Now lets see what we can do with our fully defined pynst file!

We are going to use a windows path for the scenarios, but these commands work the same on Linux or MacOS.
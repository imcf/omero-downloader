# Installation instructions

## create an environment using an Anaconda PowerShell Prompt
```
conda create --prefix S:\anaconda_envs\omero-py_env python=3.11 -y # The -y flag in conda is used to install packages without asking for confirmation
conda activate S:\anaconda_envs\omero-py_env
```

## install ZeroC IcePy 3.6 matching the python version of the environment 
- from https://www.glencoesoftware.com/blog/2023/12/08/ice-binaries-for-omero.html
```
pip install https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp311-cp311-win_amd64.whl
```

##  install omero-py. Should we install a certain version?
```
pip install omero-py==5.19.4
```

## install ttkbootstrap for a prettier GUI
```
python -m pip install ttkbootstrap
```
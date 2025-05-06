# Installation instructions

## create an environment using an Anaconda PowerShell Prompt

```bash
# The -y flag will install packages without asking for confirmation
conda create --prefix S:\anaconda_envs\omero-py_env python=3.11 -y
conda activate S:\anaconda_envs\omero-py_env
```

## install ZeroC IcePy 3.6 matching the Python version of the environment

Using the corresponding wheels provided by [Glencoe Software][1].

```bash
pip install https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp311-cp311-win_amd64.whl
```

## install omero-py

TODO: Figure out if a certain version is required.

```bash
pip install omero-py==5.19.4
```

## install ttkbootstrap for a prettier GUI

```bash
python -m pip install ttkbootstrap
```

[1]: https://www.glencoesoftware.com/blog/2023/12/08/ice-binaries-for-omero.html

# A simple OMERO downloader GUI: `omero-downloader`

## Installation instructions

The easiest way to install the tool is through [pixi], although a classical
Python `venv` setup is possible as well. In the latter case make sure to use the
ZeroC-Ice wheels provided by Glencoe ([Windows][ice-win], [Linux][ice-linux])
in order to avoid the time-consuming compilation step.

Here, we're describing the setup using `pixi`:

1. First, you'll obviously need `pixi` itself. In case you don't have it yet,
   we're recommending to download the appropriate [standalone binary][pixi-bin]
   from GitHub as this won't involve any persistent changes to your system.
1. Next, clone this repository.
1. Then, simply run `pixi install` inside the repo.

From there on, you may use `pixi` to launch the `omero-downloader-gui` tool, but
that's not a requirement. Calling it directly will also work, and is much
simpler:

```bash
# on 🐧 Linux:
$PATH_TO_REPO/.pixi/envs/default/bin/omero-downloader-gui
```

```Powershell
# on 🟦 Windows:
$PATH_TO_REPO\.pixi\envs\default\Scripts\omero-downloader-gui
```

[pixi]: https://pixi.sh/
[pixi-bin]: https://github.com/prefix-dev/pixi/releases
[ice-linux]: https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases
[ice-win]: https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases

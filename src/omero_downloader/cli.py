"""Command line entry points."""

import argparse
import sys
import ttkbootstrap as ttk

from .download import download_object
from .gui import OmeroDownloaderApp


def launch_gui():
    """Launch the GUI applications."""
    root_window = ttk.Window(themename="yeti")  # superhero
    app = OmeroDownloaderApp(root_window)
    root_window.mainloop()


def download_pdi():
    """Parse arguments and perform download tasks."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "obj", help="Download object: 'Project:ID', 'Dataset:ID' or 'Image:ID'"
    )
    parser.add_argument("target", help="Directory name to download into")
    parser.add_argument("hostname", help="OMERO server address")
    parser.add_argument("username", help="OMERO user name")
    parser.add_argument("password", help="OMERO password")
    args = parser.parse_args(sys.argv)

    download_object(args)

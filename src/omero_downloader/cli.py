"""Command line entry points."""

import click
import ttkbootstrap as ttk

from .download import download_object
from .gui import OmeroDownloaderApp


@click.command(help="Simple OMERO Downloader GUI.")
@click.option("--config", type=str, default="", help="Configuration file.")
def launch_gui(config):
    """Launch the GUI applications."""
    print("Launching OMERO Downloader GUI, might take a few moments ...")
    root_window = ttk.Window(themename="yeti")  # superhero
    app = OmeroDownloaderApp(root_window, config)
    root_window.mainloop()


@click.command(help="Download a project/dataset/image from OMERO.")
@click.option(
    "--obj", type=str, help="Download object: 'Project:ID', 'Dataset:ID' or 'Image:ID'"
)
@click.option(
    "--destination",
    type=click.Path(exists=False),
    help="Path to store downloaded files.",
)
@click.option("--server", type=str, help="OMERO server address.")
@click.option("--username", type=str, help="OMERO user name.")
@click.option("--password", type=str, help="OMERO password.")
def download_pdi(obj, destination, server, username, password):
    """Parse arguments and start download tasks."""
    print(f"Requesting {obj}")
    print(f"Selected target destination: [{destination}]")
    download_object(obj, destination, server, username, password)

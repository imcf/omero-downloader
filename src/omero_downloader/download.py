"""Functions for downloading projects / datasets / images from OMERO."""

import os
import omero.clients
from omero.gateway import BlitzGateway
from omero.plugins.download import DownloadControl

OBJ_INFO = "obj should be 'Project:ID', 'Dataset:ID' or 'Image:ID'"


def download_datasets(conn, datasets, target_dir):
    """Download all datasets and their images to the specified directory.

    Parameters
    ----------
    conn : BlitzGateway
        The connection to the OMERO server.
    datasets : list
        A list of datasets to download.
    target_dir : str
        The target directory for downloads.
    """
    for dataset in datasets:
        print(f"Downloading Dataset {dataset.id}: {dataset.name}")
        dataset_dir = os.path.join(target_dir, dataset.name)
        os.makedirs(dataset_dir, exist_ok=True)

        for image in dataset.listChildren():
            download_image_fileset(conn, image, dataset_dir)


def download_image_fileset(conn, image, target_dir):
    """Download the fileset of a single image.

    Parameters
    ----------
    conn : BlitzGateway
        The connection to the OMERO server.
    image : Image
        The image object to download.
    target_dir : str
        The target directory for the image download.
    """
    fileset = image.getFileset()
    if fileset is None:
        print(f"No files to download for Image {image.id}")
        return

    dc = DownloadControl()
    dc.download_fileset(conn, fileset, target_dir)


def download_object(obj, destination, server, username, password):
    """Download the specified object (Project, Dataset, or Image).

    Parameters
    ----------
    obj : str
    destination : Path
    server : str
    username : str
    password : str
    """
    # print(f"{obj} - {destination} - {server} - {username}")

    client = omero.client(server, 4064)
    session = client.createSession(username, password)
    with BlitzGateway(client_obj=client) as conn:
        if not conn.connect():
            print("Failed to connect to OMERO server")
            return

        print("Connected to OMERO server")

        conn.SERVICE_OPTS.setOmeroGroup(-1)

        obj_type, obj_id = parse_object_id(obj)
        parent = conn.getObject(obj_type, obj_id)

        if parent is None:
            print(f"Not Found: {obj}")
            return

        target_dir = destination
        datasets = []

        print(f"Processing [{obj}]")

        if obj_type == "Dataset":
            datasets.append(parent)
        elif obj_type == "Project":
            datasets = list(parent.listChildren())
            target_dir = os.path.join(target_dir, parent.getName())
        elif obj_type == "Image":
            download_image_fileset(conn, parent, target_dir)
            return
        else:
            print(OBJ_INFO)
            return

        print(f"Downloading to {target_dir}")
        download_datasets(conn, datasets, target_dir)


def parse_object_id(obj):
    """Parse the object ID and type from the given string.

    Parameters
    ----------
    obj : str
        The object string in the format 'Type:ID'.

    Returns
    -------
    tuple
        A tuple containing the object type and ID.

    Raises
    ------
    ValueError
        If the object string is not in the correct format.
    """
    try:
        obj_type, obj_id = obj.split(":")
        return obj_type, int(obj_id)
    except ValueError:
        raise ValueError(OBJ_INFO)

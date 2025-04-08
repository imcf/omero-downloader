import argparse, os, sys
import omero.clients
from omero.gateway import BlitzGateway
from omero.plugins.download import DownloadControl

"""
Usage:
python download_pdi.py Project:123 my_project_directory hostname username password

Notes:
this script originated from Will Moore:
https://gist.github.com/will-moore/a9f90c97b5b6f1a0da277a5179d62c5a
"""

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


def download_object(conn, args):
    """Download the specified object (Project, Dataset, or Image).

    Parameters
    ----------
    conn : BlitzGateway
        The connection to the OMERO server.
    args : Namespace
        The command line arguments containing the object and target directory.
    """
    conn.SERVICE_OPTS.setOmeroGroup(-1)

    obj_type, obj_id = parse_object_id(args.obj)
    parent = conn.getObject(obj_type, obj_id)

    if parent is None:
        print(f"Not Found: {args.obj}")
        return

    target_dir = args.target
    datasets = []

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


def main(argv):
    """Main entry point for the script.

    Parameters
    ----------
    argv : list
        The command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "obj", help="Download object: 'Project:ID', 'Dataset:ID' or 'Image:ID'"
    )
    parser.add_argument("target", help="Directory name to download into")
    parser.add_argument("hostname", help="OMERO server address")
    parser.add_argument("username", help="OMERO user name")
    parser.add_argument("password", help="OMERO password")
    args = parser.parse_args(argv)

    client = omero.client(args.hostname, 4064)  # Default OMERO port
    session = client.createSession(args.username, args.password)
    conn = BlitzGateway(client_obj=client)

    if conn.connect():
        print("Connected to OMERO server")
        download_object(conn, args)
    else:
        print("Failed to connect to OMERO server")

    conn.close()
    print("Connection closed")


if __name__ == "__main__":
    main(sys.argv[1:])

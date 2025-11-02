"""Utility functions."""

import re
import json
from pathlib import Path


def extract_datatype_and_ids(url):
    """Extract the data type and associated IDs from the given URL string.

    Parameters
    ----------
    url : str
        The URL string containing identifiers.

    Returns
    -------
    tuple
        A tuple containing:
        - data_types : list of str
            A list of data types corresponding to the prefixes found in the URL.
        - data_ids : list of str
            A list of extracted IDs

    Example
    ------
        url = "https://idr.openmicroscopy.org/webclient/?show=project-2305|project-5678"
        data_types, data_ids = extract_datatype_and_ids(url)
        print(data_types)  # Output: ['Project', 'Project']
        print(data_ids)    # Output: [2305, 5678]
    """

    prefix_to_type = {"project-": "Project", "dataset-": "Dataset", "image-": "Image"}

    # Find two groups: matches of the prefix and associated ID
    matches = re.findall(r"(project-|dataset-|image-)(\d+)", url)

    if not matches:
        print("No matches found in URL")
        return [], []

    # Extract data types and IDs from the matches
    data_types = [prefix_to_type[prefix] for prefix, _ in matches]
    data_ids = [id for _, id in matches]

    if len(data_types) == len(data_ids):
        return data_types, data_ids
    else:
        print("Number of data types and IDs don't match")
        return [], []


def load_all_db_entries(config_path):
    """Extract all database addresses from the configuration file.

    Parameters
    ----------
    config_path : str
        Path to the JSON configuration file.

    Returns
    -------
    list
        list of all database addresses
    """
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    addresses = [database["address"] for database in config["databases"].values()]

    return addresses


def get_config_path():
    """Locate the configuration file path of 'config.json'.

    Check if the current environment is using this package through an "editable"
    installation or a regular one and identify the "base" path where the config
    file is expected to be found.

    Returns
    -------
    pathlib.Path
        Path to the 'config.json' file.

    Raises
    ------
    FileNotFoundError
        If the 'config.json' file does not exist in the expected location.

    Example
    -------

    In an editable installation:

    >>> print(__file__)
    ... /opt/odl/src/omero_downloader/utils.py
    >>> print(get_config_path())
    ... /opt/odl/config.json


    In a regular installation:

    >>> print(__file__)
    ... /opt/odl/.pixi/envs/def/lib/python3.11/site-packages/omero_downloader/utils.py
    >>> print(get_config_path())
    ... /opt/odl/config.json
    """
    mod_dir = Path(__file__)
    editable = True if mod_dir.parents[1].name == "src" else False
    # print(f"Running from 'editable' installation: {editable}")
    up = 2 if editable else 7
    config_dir = mod_dir.parents[up]
    config_path = config_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Unable to find config file at: {config_path}")
    print(f"Using config file: {config_path}")

    return config_path

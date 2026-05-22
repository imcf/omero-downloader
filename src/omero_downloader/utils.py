"""Utility functions."""

import re
import sys
from pathlib import Path

import yaml

example_conf = yaml.dump(
    {
        "databases": {
            "Local": {"address": "localhost"},
            "Institute": {"address": "omero.institute.example"},
        }
    }
)


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
        config = yaml.safe_load(config_file)

    addresses = [database["address"] for database in config["databases"].values()]

    return addresses


def get_config_path(config=""):
    """Locate the configuration file path for the OMERO Downloader.

    Look at various pre-defined locations for a configuration file - see the
    **Notes** section for details and precedence on the searched locations.

    In case a path is specified explicitly, that path is validated but no search
    will be performed.

    Parameters
    ----------
    config : str, optional
        The path to a configuration file, by default "" in which case the
        function will attempt to automatically locate a config file by checking
        a number of pre-defined locations - see the **Notes** for details.

    Returns
    -------
    pathlib.Path
        Path to an OMERO-Downloader configuration file.

    Raises
    ------
    FileNotFoundError
        Thrown when no config file can be found at any of the searched locations
        or in case the provided path doesn't exist.

    Notes
    -----
    When performing the search, each location will be checked for two files in
    this order:

    * `omero-downloader.yml`
    * `config.yml`

    The **first file** that is found will be used as the configuration.

    The locations to be checked depend on the environment the package is running
    in, which is determined by the path structure where *this* file (`utils.py`)
    is located.

    Three different situations are being considered:

    (1) An "editable" installation (the parent folder two levels up is called
    `src`): the folder containing the `src` directory will be searched, which
    corresponds to the project-root when running from a cloned repository.

    (2) A "pixi global" installation (the parent folder 5 levels up is
    called `omero-downloader` and the one 6 levels up is called `envs`): config
    files will be searched in the folder `omero-downloader` and in a subfolder
    named `etc`. This corresponds to the installation location when using the
    setup approach via `pixi global install`.

    (3) A local / custom installation (when none of the above conditions match):
    the parent folder 7 levels up will be searched, plus a subfolder of it named
    `etc`. This corresponds to the root folder of the installation when using
    `pixi install` on the project itself.

    Example
    -------

    In an editable installation, e.g. like this:

    ```
    /home/user/development/
    └── omero-downloader
        ├── config.yml
        └── src
            └── omero_downloader
                └── utils.py
    ```

    >>> print(get_config_path())
    ... /home/user/development/omero-downloader/config.yml


    In a global pixi installation:

    ```
    /home/user/.pixi/
    └── envs
        └── omero-downloader
            ├── etc
            │   └── omero-downloader.yml
            └── lib
                └── python3.11
                    └── site-packages
                        └── omero_downloader
                            └── utils.py
    ```

    >>> print(get_config_path())
    ... /home/user/.pixi/envs/omero-downloader/etc/omero-downloader.yml


    In a (local) pixi installation:

    ```
    /opt/omero-downloader/
    ├── .pixi
    │   └── envs
    │       └── default
    │           └── lib
    │               └── python3.11
    │                   └── site-packages
    │                       └── omero_downloader
    │                           └── utils.py
    └── etc
        └── omero-downloader.yml
    ```

    >>> print(get_config_path())
    ... /opt/omero-downloader/etc/omero-downloader.yml
    """
    locations = []
    config_path = None

    if config != "":
        locations.append(Path(config).absolute())
    else:
        print("No config file specified, trying to find it ourselves...")
        # check a few locations for the config file, depending on where *this*
        # file is actually located:
        mod_dir = Path(__file__).absolute()
        # print(f"mod_dir: {mod_dir}")

        pixi_global = False
        editable = False

        src_dir = mod_dir.parents[1].name
        # print(f"Checking for 'src' dir: {src_dir}")
        if src_dir == "src":
            editable = True
            print("Found 'src' dir, assuming editable installation.")
            locations.append(mod_dir.parents[2] / "omero-downloader.yml")
            locations.append(mod_dir.parents[2] / "config.yml")

        # on Windows, nesting is one level less as envs don't seem to have a
        # Python-version-specific folder above "site-packages", so adjust:
        proj_up = 4 if sys.platform != "win32" else 3
        proj_dir = mod_dir.parents[proj_up].name
        envs_dir = mod_dir.parents[proj_up + 1].name
        # print(f"Checking project and envs dirs: '{proj_dir}' / '{envs_dir}'")
        if proj_dir == "omero-downloader" and envs_dir == "envs":
            pixi_global = True
            print("Found dirs expected in a 'pixi global' installation.")
            locations.append(mod_dir.parents[proj_up] / "omero-downloader.yml")
            locations.append(mod_dir.parents[proj_up] / "config.yml")
            locations.append(mod_dir.parents[proj_up] / "etc" / "omero-downloader.yml")
            locations.append(mod_dir.parents[proj_up] / "etc" / "config.yml")

        if not pixi_global and not editable:
            print("Assuming local / custom installation.")
            locations.append(mod_dir.parents[7] / "omero-downloader.yml")
            locations.append(mod_dir.parents[7] / "config.yml")
            locations.append(mod_dir.parents[7] / "etc" / "omero-downloader.yml")
            locations.append(mod_dir.parents[7] / "etc" / "config.yml")

    for candidate in locations:
        print(f"Checking for config file at: {candidate}")
        if candidate.exists():
            config_path = candidate
            break

    if not config_path:
        print("\n===== ERROR: unable to find config file, stopping! =====\n")
        raise FileNotFoundError

    print(f"Using config file: {config_path}")

    return config_path

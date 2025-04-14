import re


def extract_datatype_and_ids(url):
    """
    Extract the data type and associated IDs from the given URL string.

    Parameters
    ----------
    url : str
        The URL string containing identifiers.

    Returns
    -------
    tuple
        A tuple containing:
        - data_type : str
            The data type corresponding to the prefix found in the URL.
        - data_ids : list of int
            A list of extracted IDs as integers.

    Notes
    -----
    The function assumes that the prefixes 'project-', 'dataset-', and 'image-'
    are mutually exclusive within the URL.

    Example
    ------
    url = "https://omero.biozentrum.unibas.ch/webclient/?show=project-2305|dataset-5678"
    data_type, data_ids = extract_datatype_and_ids(url)
    print(data_type)  # Output: Project
    print(data_ids)   # Output: [2305, 5678]
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

    return data_types, data_ids

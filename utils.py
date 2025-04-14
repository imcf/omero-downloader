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
        - data_types : list of str
            A list of data types corresponding to the prefixes found in the URL.
        - data_ids : list of str
            A list of extracted IDs

    Example
    ------
    url = "https://omero.biozentrum.unibas.ch/webclient/?show=project-2305|project-5678"
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

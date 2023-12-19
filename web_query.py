import requests
import numpy as np
from londontube.network import Network
from datetime import datetime
from urllib.parse import quote

def query_line_connectivity(line_id):
    """
    Query and retrieve line connectivity information.

    Args:
        line_id (int): The ID of the line to query.

    Returns:
        list: A list of lists containing connectivity information for the specified line.

    Example:
    .. code-block:: python

        # Example usage of query_line_connectivity
        line_id = 1  # Example line ID for query
        connectivity_info = query_line_connectivity(line_id)
        print(connectivity_info)

    """
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_id}")
    lines = response.text.strip().split('\n')
    network_data = [list(map(int, line.split(','))) for line in lines]
    return network_data
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

def station_information(line_id):

    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={line_id}")
    lines = response.text.strip().split('\n')
    
    stations_data = []
    for line in lines[1:]:  # Skip the first line 
        parts = line.split(',')
        
        #Design for Heathrow Terminals 1
        if len(parts) > 4:
            del parts[2]
        
        # Clean up station names by removing unwanted symbols and trimming spaces
        station_name = parts[1].replace('&', 'and').replace('"', '').strip()
        # Add other necessary parts if there are more details to be included
        stations_data.append([parts[0], station_name] + parts[2:])
        
    return stations_data
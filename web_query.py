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
    """
    Retrieve information about London Tube stations for a specific line or all lines.

    Args:
        line_id (str): The identifier for the line to query. Use 'all' to retrieve information for all stations.

    Returns:
        list: A list of lists containing station information. Each inner list includes station attributes in the following order:
            1. Station ID
            2. Station Name
            3. Station Coordinate
    """
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

def update_matrix_disruption(weight_matrix, date=None):
    """
    Update the weight matrix based on disruption information for a given date.

    Args:
        weight_matrix (numpy.ndarray): The original weight matrix representing station connectivity.
        date (str): The date for which disruption information is to be considered.

    Returns:
        numpy.ndarray: The updated weight matrix with disruption effects applied.
    
    Example:
    .. code-block:: python

        # Example usage of update_matrix_disruption
        weight_matrix = np.array([[0, 1], [1, 0]])  # Example weight matrix
        date = '2023-01-01'  # Example date
        updated_matrix = update_matrix_disruption(weight_matrix, date)
        print(updated_matrix)
    """
    #Check if there is no date, return the original weight matrix
    if date is None:
        return weight_matrix
    
    #Feteching the distuption data from API
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/disruptions/query?date={date}")
    if response.status_code != 200:
        raise Exception("Failed to get disruption information")
    
    disruptions = response.json()
    for disruption in disruptions:
        stations = disruption.get('stations')
        
        delay = disruption.get('delay', 1)  # Ensure delay is a valid number

        if delay <= 0:  # Handle invalid delays, skip processing
            continue

        if len(stations) == 1: #Handle one station failure
            station = stations[0]
            weight_matrix[station, :] = np.inf  # Close all connections to this station
            weight_matrix[:, station] = np.inf
        
        elif len(stations) == 2: #Handling delays between 2 stations
            station1, station2 = stations # Ensuring station indices are within the bounds of the matrix
            
            if 0 <= station1 < len(weight_matrix) and 0 <= station2 < len(weight_matrix):
                # Apply delay to the weights between the two stations
                weight_matrix[station1][station2] *= delay
                weight_matrix[station2][station1] *= delay
                # If the resulting weights are zero or negative, set them to infinity (indicating no viable path)
                if weight_matrix[station1][station2] <= 0 or weight_matrix[station2][station1] <= 0:  # Handle zero or negative weights
                    weight_matrix[station1][station2] = np.inf
                    weight_matrix[station2][station1] = np.inf

    return weight_matrix

def journey_planner(start, destination, setoff_date=None): #default date is none

    stations_data = station_information('all') #get all stations information
    station_names = [station[1] for station in stations_data] #extract names from the station information

    #Convert names to indices
    start_index = station_names.index(start) if start in station_names else int(start)
    destination_index = station_names.index(destination) if destination in station_names else int(destination)

    #Determine the number of stations
    n_max = len(stations_data)
    weight_matrix = np.zeros((n_max, n_max)) # Initialize the weight matrix with zeros
    allweight_inf = []
    
    # Collect connectivity information for each line
    for i in range(12):
        allweight_inf += query_line_connectivity(i)
        
    # Populate the weight matrix with connectivity information
    for a, b, weight in allweight_inf:
        weight_matrix[a][b] = weight
        weight_matrix[b][a] = weight
        
    # Use the current date if no setoff date is provided
    setoff_date = setoff_date or datetime.now().strftime('%Y-%m-%d')
    
    # Update the matrix with disruption information
    updated_matrix = update_matrix_disruption(weight_matrix, setoff_date)

    # Initialize network instances for original and updated matrices
    original_network = Network(weight_matrix)
    updated_network = Network(updated_matrix)
    
    # Compute the shortest path using Dijkstra's algorithm
    original_path, original_cost = original_network.dijkstra(start_index, destination_index)
    updated_path, updated_cost = updated_network.dijkstra(start_index, destination_index)
    
    # Handle the case where a path is not available due to disruptions
    if original_path is None:
        if updated_path is None:
            return{"message":"Journey is not possible due to disruptions."}
        else:
            return {
                "message": f"Journey will take {updated_cost} minutes.\nStart: {start}\n{' -> '.join(station_names[i] for i in updated_path)}\nEnd: {destination}",
                "path": updated_path,
                "station_names": station_names}
    else:
        return {
            "message": f"Journey will take {original_cost} minutes.\nStart: {start}\n{' -> '.join(station_names[i] for i in original_path)}\nEnd: {destination}",
            "path": original_path,
            "station_names": station_names
        }

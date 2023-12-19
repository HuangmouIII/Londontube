import requests
import numpy as np
import re
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
    if isinstance(line_id, str) and line_id.startswith("mock"):
        line_id_int = line_id  # Keep line_id as a string for simulating requests
    else:
        try:
            line_id_int = int(line_id)  # Try to convert line_id to an integer
        except ValueError:
            raise ValueError(f"Invalid line ID: {line_id}")

        # Validate if line_id is within a valid range
        if not 0 <= line_id_int <= 11:
            raise ValueError("Line ID must be between 0 and 11 inclusive")

    # Make a request to get line connectivity information
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_id}")

    if response.status_code != 200:
        raise Exception("Failed to get line connectivity information")

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
    
    if response.status_code != 200:
        raise Exception("Failed to get station information")
    
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
    
    # Transform to array form
    weight_matrix = np.array(weight_matrix)

    # Make a request to get disruption information based on the date
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/disruptions/query?date={date}")
    # Raise value when failed to get info
    if response.status_code != 200:
        raise Exception("Failed to get disruption information")

    disruptions = response.json()
    for disruption in disruptions:
        stations = disruption.get('stations')
        delay = disruption.get('delay', 1)

        if delay <= 0:  # Single station closure condition
                station = stations[0]
                weight_matrix[station, :] = 0
                weight_matrix[:, station] = 0
        
        elif len(stations) == 2:  # Delay between two stations 
                station1, station2 = stations
                weight_matrix[station1, station2] = delay
                weight_matrix[station2, station1] = delay

    # Convert the NumPy array back to a list
    return weight_matrix.tolist()

def journey_planner(start, destination, setoff_date=None): #default date is none
    """
    Plan a journey from a starting station to a destination station, considering disruptions.

    Args:
        start (str or int): The starting station name or index.
        destination (str or int): The destination station name or index.
        setoff_date (str, optional): The date of the journey. Defaults to None.

    Returns:
        dict: A dictionary containing journey information including duration, path, and station names.
    
    Example:
        >>> journey_planner('Aldgate', 'Angel')
        {'message': 'Journey will take 10 minutes.', 'path': [1, 2], 'station_names': ['Aldgate', 'Angel']}
    
    """
    # Regular expression pattern to match the date format 'YYYY-MM-DD'
    date_format_regex = r'^\d{4}-\d{2}-\d{2}$'

    # Check if 'setoff_date' is provided and if it matches the expected format
    if setoff_date and not re.match(date_format_regex, setoff_date):
        raise ValueError("Date must be of the format YYYY-MM-DD")

    # If 'setoff_date' is not provided, set it to the current date in 'YYYY-MM-DD' format
    setoff_date = setoff_date or datetime.now().strftime('%Y-%m-%d')

    # Define valid start and end dates as datetime objects
    valid_start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    valid_end_date = datetime.strptime("2024-12-31", "%Y-%m-%d")

    try:
        # Try to convert 'setoff_date' to a datetime object
        actual_date = datetime.strptime(setoff_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be of the format YYYY-MM-DD")

    # Check if 'actual_date' is within the valid date range (inclusive)
    if not (valid_start_date <= actual_date <= valid_end_date):
        raise ValueError("Date must be between 2023-01-01 and 2024-12-31 inclusive")

    stations_data = station_information('all') #get all stations information
    station_names = [station[1] for station in stations_data] #extract names from the station information

    try:
        # Try to convert 'start' and 'destination' to integers if they are not in 'station_names'
        start_index = int(start) if start not in station_names else station_names.index(start)
        destination_index = int(destination) if destination not in station_names else station_names.index(destination)
    except ValueError:
        raise ValueError("Invalid station ID")

    # Validate whether station indexes are within a valid range
    if not (0 <= start_index < len(stations_data)) or not (0 <= destination_index < len(stations_data)):
        raise ValueError("Station ID must be between 0 and 295 inclusive")
    
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
            #if both path are not exist that means this journey is not possible
            return{"message":"Journey is not possible due to disruptions."}
        else:
            #update the path for the new line 
            return {
                "message": f"Journey will take {updated_cost} minutes.\nStart: {start}\n{' -> '.join(station_names[i] for i in updated_path)}\nEnd: {destination}",
                "path": updated_path,
                "station_names": station_names}
    #normal situation
    else:
        return {
            "message": f"Journey will take {original_cost} minutes.\nStart: {start}\n{' -> '.join(station_names[i] for i in original_path)}\nEnd: {destination}",
            "path": original_path,
            "station_names": station_names
        }
        
def query_line_connectivity1(line_id):
    """
    Queries the connectivity data of a specific tube line based on its identifier.

    This function sends a GET request to a web service to retrieve the network data
    for a specified tube line in London. The data is processed and returned as a list
    of lists, where each inner list contains integer values representing connectivity
    information.

    Args:
    line_id (str): A unique identifier for the tube line whose data is to be queried.

    Returns:
    list of lists: Network data representing connectivity of the tube line. Each sublist
    contains integers representing specific connectivity information.

    Raises:
    ValueError: If the tube line with the specified identifier does not exist (HTTP 404 error).
    Exception: For any other HTTP errors encountered during the request.

    Note:
    The function relies on a specific external service URL and expects a specific response format.
    """
# Send a GET request to the service
    response = requests.get(
        f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_id}")
# Check the HTTP response status code
    if response.status_code == 404: # 404 Not Found
        raise ValueError(f"Line with identifier '{line_id}' does not exist.")
    elif response.status_code != 200:
        raise Exception(f"Failed to retrieve data for line {line_id}. Status code: {response.status_code}")
# Process the response text
    lines = response.text.strip().split('\n')
    network_data = [list(map(int, line.split(','))) for line in lines]
    return network_data

def station_information1(line_id):
    """
    Retrieves information about the stations on a specific tube line based on its identifier.

    This function sends a GET request to a web service to fetch information about the
    stations on a given tube line. The response is parsed into a list of lists, where
    each inner list represents data for a single station.

    Args:
    line_id (str): A unique identifier for the tube line whose station data is to be queried.

    Returns:
    list of lists: Data about the stations on the specified tube line. Each sublist contains
    station information, typically as strings.

    Raises:
    ValueError: If no station with the specified identifier exists (HTTP 404 error).
    Exception: For any other HTTP errors encountered during the request.

    Note:
    The function encodes the `line_id` parameter to handle special characters in URLs. It also
    assumes a specific response format from the external service.
    """
    encoded_line_id = quote(line_id)
    response = requests.get(f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={encoded_line_id}")

# Check the HTTP response status code
    if response.status_code == 404: # Not Found
        raise ValueError(f"Station with identifier '{line_id}' does not exist.")
    elif response.status_code != 200:
        raise Exception(f"Failed to retrieve data for station {line_id}. Status code: {response.status_code}")

    stations_data = [line.split(',') for line in response.text.strip().split('\n')[1:]]
    return stations_data

import re
import argparse
import matplotlib.pyplot as plt
from londontube.web_query import journey_planner, station_information

#from network import Network
#from web_query import station_information

#Station index
#get_index = station_information('Vauxhall')[0][0]

#Station name
#get_name = station_information('Vauxhall')[0][1]

#Station latitude
#get_lat = station_information('Vauxhall')[0][2]

#Station lontitude
#get_lon = station_information('Vauxhall')[0][3]

"""
This module provides functionality to plan journeys on the London Tube network.
It includes functions to plot journey paths, clean data, and convert station indices to names.

"""

#Function to transfer the index to name
def get_station_name(station_index):
    """
    Get the name of a station based on its index.

    Args:
        station_index (int): The index of the station.

    Returns:
        str or None: The name of the station if found, or None if the index is invalid.
    
    Example:
        >>> get_station_name(10)
        'King's Cross St Pancras'
    """
    stations_data = station_information('all')
    station_names = [station[1] for station in stations_data] # Extract the names from station data


    try:
        return station_names[int(station_index)]
    except (ValueError, IndexError): # If index is invalid or not found, return None
        return None
    
    #This is the function design for['116', 'Heathrow Terminals 1', ' 2  3', '51.4713', '-0.4524']    
def clean_data(data):
    """
    Clean and preprocess station data.

    Args:
        data (list): A list of station data records.

    Returns:
        list: Cleaned and preprocessed station data.

    Example:
        >>> clean_data([[116, 'Heathrow Terminals 1', '2 3', '51.4713', '-0.4524']])
        [[116, 'Heathrow Terminals 1', '51.4713', '-0.4524']]
    """
    cleaned_data = []
    for record in data:
        # If the recorded elements > 4, delete the third one (2&3)
        if len(record) > 4:
            del record[2]
        
        # Clean the rubbish
        record = [re.sub(r'[&"]', '', str(item)) for item in record]
        cleaned_data.append(record)

    return cleaned_data

#Function to plot    
def plot_journey(path, station_names):
    """
    Plot a journey path on a map. First plot all the stations in the map and the connect the path
    with a blue line.

    Args:
        path (list): A list of station indices representing the journey path.
        station_names (list): A list of station names corresponding to station indices.

    Returns:
        None

    """
    # Extract coordinates for all stations
    all_station_coordinates = []
    stations_data = station_information("all")
    cleaned_data = clean_data(stations_data)
    
   
        
    for station in cleaned_data:
        try:
            lat = float(station[2])
            lon = float(station[3])
            all_station_coordinates.append((lat, lon))
        except ValueError as e:
                print(f"Error converting station: {station}")

    plt.figure(figsize=(12, 8))

    # Plot all stations as black points
    all_lats, all_lons = zip(*all_station_coordinates)
    plt.scatter(list(map(float, all_lons)), list(map(float, all_lats)), color='black', marker='o')

    # Plot the journey path as a continuous line
    journey_coordinates = [(float(station_information(station)[0][3]), float(station_information(station)[0][2])) for station in path]
    journey_lons, journey_lats = zip(*journey_coordinates)
    
    # Plot the route
    plt.plot(list(map(float, journey_lons)), list(map(float, journey_lats)), color='blue', linestyle='-', linewidth=1.8)

    plt.title(f'Journey from {station_names[path[0]]} to {station_names[path[-1]]}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Save the plot as a file
    plt.savefig(f"journey_from_{station_names[path[0]].replace(' ', '_')}_{station_names[path[-1]].replace(' ', '_')}.png")
    
    plt.show()



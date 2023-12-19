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


# Main function
def main():
    """
    Main function that serves as the entry point for the journey planner tool.

    .. note:: Replace "&" with "and" if the name of station contains it, 
              no symbols like [" ' ? .] will be acceptable.

              'Heathrow Terminals 1' stands for 'Heathrow Terminals 1, 2 & 3'. 
              When starting or ending at these terminals, only type "Heathrow Terminals 1".

    :return: None
    
    Input requirements

    Compulory input:
    1.For start station, the index of the station or the name of station can be as the input.
    2.For destination station, the index of the station or the name of station can be as the input.
    
    Optional input:
    3.If you do not write the departure date, it will be the same day by default, and if you need to add the date, you need to follow the following format: YYYY-MM-DD
    4.--plot is the plot function
    
    Genenral input format:[--plot] ["start station name/index"] ["destination station name/index"] [setoff date]
    
    Notice when using:
    Important notice 1: Replace "&" with "and" if the name of station contains, no symbol like [" ' ? .] will be accepetable
    Important notice 2: The  'Heathrow Terminals 1' is stand for  'Heathrow Terminals 1  2 & 3' When start/destination is Heathrow Terminals 1  2 & 3, only need to type "Heathrow Terminals 1"
    
    """
    parser = argparse.ArgumentParser(description="Journey Planner Tool") # Define arguments for the parser
    parser.add_argument("start", help="Start station or index")
    parser.add_argument("destination", help="Destination station or index")
    parser.add_argument("setoff_date", nargs="?", default=None, help="Setoff date")
    parser.add_argument("--plot", action="store_true", help="Enable plotting")
    
    # Parse arguments from the command line
    args = parser.parse_args()

    # Convert station indexes to station names
    start_station = get_station_name(args.start) if args.start.isdigit() else args.start
    destination_station = get_station_name(args.destination) if args.destination.isdigit() else args.destination

    # If the index is out of range, raise an error
    if start_station is None or destination_station is None:
        raise ValueError("Station ID must be between 0 and 295 inclusive")

    # Call the journey_planner function
    result = journey_planner(start_station, destination_station, args.setoff_date)
    
    # Check if the journey is possible
    if "Journey is not possible due to disruptions." in result["message"]:
        print(result["message"])
    
    else:
        print(result["message"])
    

        if args.plot:
           plot_journey(result["path"], result["station_names"])
           
if __name__ == "__main__":
    main()
    

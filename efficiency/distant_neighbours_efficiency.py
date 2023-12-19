import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import timeit
from londontube.web_query import query_line_connectivity1, station_information1
from londontube.network import Network
"""
Compare two method running speed for two function Distant Neighbours funtion - User Guide

Prerequisites:

Python libraries: NumPy, Matplotlib, Pandas ,timeit
Install Libraries (if needed): londontube package

Copy code
pip install numpy matplotlib pandas
Script Overview:

Fetches station data and connectivity data for the London Tube network.
Populates a weight matrix with the fetched data.
Analyzes performance of two methods:
weight_matrix_network.distant_neighbours()
provided_distant_neighbours()

Usage:
Modify station_list to include desired stations.
Calculate speed for two method and plot which one is faster.

Output:
Execution times written to distant_neighbours_times.md.
Performance plot displayed with logarithmic scales.
Note:

Ensure the londontube package is properly installed.
Contact support for any issues or questions.

"""
def provided_distant_neighbours(n, v, adjacency_matrix):
    neighbours = [v]
    for i in range(n):
        new_neighbours = []
        for index in neighbours:
            row = adjacency_matrix[index]
            for j in range(len(row)):
                if (row[j] > 0) and (j not in neighbours) and (j not in new_neighbours):
                    new_neighbours.append(j)
        neighbours += new_neighbours
    while v in neighbours:
        neighbours.remove(v)
    return neighbours

# Gathering station data and preparing the weight matrix
stations_data = len(station_information1('all'))
n_max = stations_data

weight_matrix = np.zeros((n_max,n_max))
allweight_inf= []

# Populating the weight matrix with connectivity data
for i in range(12):
    allweight_inf += query_line_connectivity1(i)

for i in range(len(allweight_inf)):
    a, b, weight = allweight_inf[i]
    weight_matrix[a][b] = weight
    weight_matrix[b][a] = weight

weight_matrix_network = Network(weight_matrix)
# Preparing test stations
station_list = ['Baker Street', 'Blackfriars', 'Cockfosters', "Earl's Court", 'Elephant & Castle', 'Finsbury Park', "King's Cross St. Pancras", 'Morden', 'Vauxhall']
test_stations = [int(station_information1(i)[0][0]) for i in station_list]

# Defining the range of n values for testing
n_values = [1, 2, 3, 4, 5, 7, 8, 10, 12, 14, 17, 20, 25, 29, 35, 42, 51, 61, 73, 87, 104, 125, 149, 179, 214, 256]

# Initializing results dictionary to store performance data
results = {station: {'new_method': [0]*len(n_values), 'provided_method': [0]*len(n_values)} for station in test_stations}

# Performing tests and collecting data
for station in test_stations:
    for i, n in enumerate(n_values):
        time_network = timeit.timeit(lambda: weight_matrix_network.distant_neighbours(n, station), number=10)
        results[station]['new_method'][i] += time_network

        time_network1 = timeit.timeit(lambda: provided_distant_neighbours(n, station,weight_matrix), number=10)
        results[station]['provided_method'][i] += time_network1

# Writing individual station results to a Markdown file
columns = ['N Value', 'New Method Time (s)', 'Provided Method Time (s)']
with open('distant_neighbours_times.md', 'a') as file:
    for station in test_stations:
        data = []
        for i, n in enumerate(n_values):
            row = [n, results[station]['new_method'][i], results[station]['provided_method'][i]]
            data.append(row)
        df = pd.DataFrame(data, columns=columns)
        file.write(f"\n## Times for Station {station}\n")
        file.write(df.to_markdown(index=False))

# Calculating average times across all stations for plotting
average_new_method_times = [0]*len(n_values)
average_provided_method_times = [0]*len(n_values)
for i in range(len(n_values)):
    sum_new_method = sum(results[station]['new_method'][i] for station in test_stations)
    sum_provided_method = sum(results[station]['provided_method'][i] for station in test_stations)
    average_new_method_times[i] = sum_new_method / len(test_stations)
    average_provided_method_times[i] = sum_provided_method / len(test_stations)

# Plotting average performance comparison across stations
plt.figure(figsize=(10, 6))
plt.plot(n_values, average_new_method_times, label='Average My Network.distant_neighbours')
plt.plot(n_values, average_provided_method_times, label='Average Provided distant_neighbours')
plt.xlabel('n values')
plt.ylabel('Average Time (seconds)')
plt.title('Average Performance Comparison Across Stations')
plt.legend()
plt.yscale('log')
plt.xscale('log')
plt.show()


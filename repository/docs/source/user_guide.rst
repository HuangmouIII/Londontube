User Guide
==========

This guide will walk you through the basics of using LondonTube to navigate the network.


Basic Usage
-----------

.. code-block:: python

  from londontube.network import Network
  from londontube.web_query import query_line_connectivity
  # All stations for the special line
  from londontube.web_query import station_information
  # Station information
  from londontube.web_query import update_matrix_disruption
  # Update matrix information for disruption



Network Class User Guide
------------------------

The ``Network`` class is designed to represent and manipulate networks represented by adjacency matrices. Below are details of the class methods and their usage.

Constructor
^^^^^^^^^^^^

- ``__init__(self, adjacency_matrix)``
  Initializes a ``Network`` object with the given adjacency matrix.
  :param adjacency_matrix: A square matrix representing the network's adjacency.

Properties
^^^^^^^^^^
- ``n_nodes``
  Returns the number of nodes in the network.
- ``adjacency_matrix``
  Returns the adjacency matrix of the network. It checks for squareness, non-negative values, and symmetry (for undirected graphs).

Methods
^^^^^^^^
- ``__add__(self, other)``
  Combines two networks into a single network. The method merges adjacency matrices by taking the minimum non-zero value at each position.
  :param other: Another ``Network`` object to combine with.

- ``distant_neighbours(self, n, v)``
  Finds neighbours at a distance 'n' from a given node 'v'.
  :param n: The distance level.
  :param v: The node index to start from.

- ``dijkstra(self, start, destination)``
  Implements Dijkstra's algorithm to find the shortest path between two nodes.
  :param start: The starting node index.
  :param destination: The destination node index.
  :returns: A tuple containing the shortest path and its total cost.

Network Class Usage Examples
-----------------------------

Creating a Network Object
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    adjacency_matrix = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    network = Network(adjacency_matrix)
    print(network.adjacency_matrix)
    # results: [[0, 1, 0], [1, 0, 1], [0, 1, 0]]


Combining Networks
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    network1 = Network([[0, 1, 0, 0], [1, 0, 2, 0],[0, 2, 0, 0], [0, 0, 0, 0]])
    network2 = Network([[0, 0, 0, 3], [0, 0, 0, 1], [0, 0, 0, 0], [3, 1, 0, 0]])
    combined_network = network1 + network2
    print(combined_network.adjacency_matrix)
    # results: [[0, 1, 0, 3], [1, 0, 2, 1], [0, 2, 0, 0], [3, 1, 0, 0]]

Finding Distant Neighbours
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    neighbours = network.distant_neighbours(1, 0)  # Finds neighbours of node 0 at distance 1
    print(neighbours) 
    # results: [1]

Using Dijkstra's Algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    path, cost = network.dijkstra(0, 2)  # Finds shortest path from node 0 to node 2
    print(path, cost) 
    # results: [0, 1, 2] 2


journey_planner User Guide
---------------------------

The journey_planner module is designed to help users plan their journeys across the London Tube network. It includes functions to find station names based on index, clean up station data, plot journey paths, and plan journeys considering possible disruptions.

Finding Station Names
^^^^^^^^^^^^^^^^^^^^^^

To find the name of a station by its index, use the `get_station_name` function:

.. code-block:: python

    from londontube.journey_planner import get_station_name
    station_name = get_station_name(10)
    print(station_name)

This will output the name of the station associated with the index `10`.

Cleaning Station Data
^^^^^^^^^^^^^^^^^^^^^^

To clean and preprocess station data, use the `clean_data` function:

.. code-block:: python

    from londontube.journey_planner import clean_data
    cleaned_data = clean_data([[116, 'Heathrow Terminals 1', '2 3', '51.4713', '-0.4524']])
    print(cleaned_data)

This function will process the input data and output a cleaned version.

Plotting a Journey Path
^^^^^^^^^^^^^^^^^^^^^^^^

You can plot a journey path using the `plot_journey` function. This function takes a path represented by a list of station indices and plots it:

.. code-block:: python

    from londontube.journey_planner import plot_journey
    plot_journey([125, 251], ['Holborn', 'Tooting Broadway'])

Planning a Journey
^^^^^^^^^^^^^^^^^^^^

To plan a journey, you can call the `journey_planner` function with the start and destination stations:

.. code-block:: python

    from londontube.journey_planner import journey_planner
    journey_info = journey_planner('Holborn', 'Tooting Broadway')
    print(journey_info)

If the journey is possible, it will print the journey details, including the duration and path.

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^^

The journey planner can also be used via the command line. For example:

.. code-block:: bash

    journey-planner --plot "Northwood Hills" Upminster 2023-01-01

This command will plan a journey from Holborn to Tooting Broadway and plot the path if the `--plot` option is included.

Remember to replace special characters like `&` with `and` when inputting station names. For Heathrow Terminals, simply use "Heathrow Terminals 1" for the combined terminals



web_query User Guide
---------------------




distant_neighbours_efficiency Usage and Reproducibility
--------------------------------------------------------

Compare two method running speed for two function Distant Neighbours funtion - User Guide

Prerequisites:
^^^^^^^^^^^^^^^

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

Usage
^^^^^^
Modify station_list to include desired stations.
Calculate speed for two method and plot which one is faster.

Output
^^^^^^^
Execution times written to distant_neighbours_times.md.
Performance plot displayed with logarithmic scales.

Note
^^^^
Ensure the londontube package is properly installed.
Contact support for any issues or questions.
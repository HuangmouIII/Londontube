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



web_query User Guide
---------------------



distant_neighbours_efficiency User Guide
-----------------------------------------


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
import heapq
class Network:
    """
    A class to represent london tube network with an adjacency matrix as the input.

    This class provides a representation of a network with nodes and edges, 
    where edges are represented by the weights in the adjacency matrix. 
    It analyses and plans routes on (an approximation to) the London underground, 
    accounting for closures and disruptions to the network. 
    For example, find the shortest path between nodes 
    and modifying the graph in the case of service disruptions.

    Attributes:
        _adjacency_matrix (list of tuple of int): A square matrix representing 
        the edges between nodes in the network. Each cell [i][j] represents 
        the edge weight from node i to node j, with 0 indicating no edge, 
        and a positive integer indicating the edge's weight.

    Methods:
        n_nodes: Get the number of nodes in the network.
        adjacency_matrix: Retrieve the adjacency matrix.
        __add__: Combines two network instances into one by combining their adjacency matrices.
        distant_neighbours: Find nodes at a specified distance from a given node.
        provided_distant_neighbours: The provided method for finding distant neighbours.
        dijkstra: Implements Dijkstra's algorithm to find the shortest path and corresponding cost between nodes.

    Example:
        >>> network = Network([[0, 1], [1, 0]])
        >>> network.n_nodes
        2
        >>> network.adjacency_matrix
        [[0, 1], [1, 0]]

    Note:
        The adjacency matrix must be a square matrix with non-negative values. 
        For undirected graphs or networks, the matrix must also be symmetric.

    """
    
    def __init__(self, adjacency_matrix):
        """
        Initialize the Network with an adjacency matrix.

        Args:
            adjacency_matrix (list of tuple of int): A square matrix where the 
            value at adjacency_matrix[i][j] represents the weight of the edge 
            from node i to node j.

        Raises:
            ValueError: If the adjacency matrix is not square, not symmetric, 
            or contains negative values..
        """
        # Check if the matrix is square
        self._adjacency_matrix = adjacency_matrix

        n = len(self._adjacency_matrix)
        if any(len(row) != n for row in self._adjacency_matrix):
            raise ValueError("Adjacency matrix must be square.")

        # Check for non-negative values
        if any(any(cell < 0 for cell in row) for row in self._adjacency_matrix):
            raise ValueError("Adjacency matrix must have non-negative values.")

        # Check for symmetry if the graph is undirected
        if any(self._adjacency_matrix[i][j] != self._adjacency_matrix[j][i] for i in range(n) for j in range(n)):
            raise ValueError("Adjacency matrix must be symmetric for undirected graphs.")

    @property
    def n_nodes(self):
        """
        Retrieve the number of nodes in the network.

        Returns:
            int: The number of nodes.
        
        Doctest:
            >>>




        """

        return len(self._adjacency_matrix)

    @property
    def adjacency_matrix(self):
        """
        Get the adjacency matrix of the network.

        This method validates the matrix to ensure it is square, symmetric 
        (for undirected graphs), and contains only non-negative weights.

        Returns:
            list of tuple of int: The adjacency matrix of the network.

        Raises:
            ValueError: If the adjacency matrix is not square, not symmetric, 
            or contains negative values.
        """
        return self._adjacency_matrix

    def __add__(self, other):
        """
        Combines the adjacency matrix of this network with another network's 
        adjacency matrix. The combined network has an adjacency matrix formed by 
        taking the element-wise minimum of the adjacency matrices of the sub-networks.
        When taking the minimum, values of 0 is ignored due to not existing edge.

        Args:
            other (Network): Another Network object to combine with

        Returns:
            Network: A new Network instance with the combined other (Network).

        Raises:
            TypeError: If the other object is not an instance of Network.
            ValueError: If the networks have a different number of nodes.
        """

        # Check if the other object is also an instance of Network
        if not isinstance(other, Network):
            raise TypeError("Both objects must be instances of Network")

        # Ensure both networks have the same number of nodes
        if self.n_nodes != other.n_nodes:
            raise ValueError("Both networks must have the same number of nodes")

        # Initialize an empty list to store the combined adjacency matrix
        combined_matrix = []

        # Iterate over rows of both adjacency matrices simultaneously
        for row_self, row_other in zip(self.adjacency_matrix, other.adjacency_matrix):
            combined_row = []  # Initialize a new row for the combined matrix

            # Iterate over elements of both rows simultaneously
            for val_self, val_other in zip(row_self, row_other):
                # If one of the values is 0, use the other value (ignoring zeros)
                if val_self == 0:
                    combined_row.append(val_other)
                elif val_other == 0:
                    combined_row.append(val_self)
                else:
                    # If neither value is zero, take the minimum
                    combined_row.append(min(val_self, val_other))

            # Append the combined row to the combined matrix
            combined_matrix.append(combined_row)

        # Return a new Network object with the combined adjacency matrix
        return Network(combined_matrix)

    


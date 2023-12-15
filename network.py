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




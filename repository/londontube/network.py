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

    def distant_neighbours(self, n, v):
        """
        The new method to compute the n-distant neighbours of a particular node v,
        excluding the node 'v' itself

        Args:
            n (int): The distance from the node.
            v (int): The index of the node.

        Returns:
            list: A list of nodes at distance 'n' from node 'v'.

        Raises:
            ValueError: If the node index 'v' is out of bounds (v exceeds the total number of nodes).

        """

        # Check if the node index is within the bounds of the network
        if v >= self.n_nodes:
            raise ValueError("Node index out of bounds")

        # Initialize a list to keep track of visited nodes; all set to False initially
        visited = [False] * self.n_nodes

        # Mark the initial node as visited
        visited[v] = True

        # Set to keep track of nodes in the current level (distance)
        current_level = {v}

        # Loop to find neighbors at each distance level up to n
        for _ in range(n):
            next_level = set()  # Set to hold neighbors of the next level
            for node in current_level:
                # Iterate over each neighbor of the current node
                for neighbor, edge in enumerate(self.adjacency_matrix[node]):
                    # Check if there is an edge and the neighbor hasn't been visited
                    if edge > 0 and not visited[neighbor]:
                        next_level.add(neighbor)  # Add neighbor to the next level
                        visited[neighbor] = True  # Mark the neighbor as visited
            current_level = next_level  # Move to the next level

        # If n > 0, the initial node is not a neighbor of itself; remove it
        if n > 0:
            visited[v] = False

        # Compile the list of neighbors from the visited flags
        neighbours = [i for i, reached_node in enumerate(visited) if reached_node]

        # Return the sorted list of neighbors
        return neighbours

   
    def dijkstra(self, start, destination):
        """
        Implement Dijkstra's algorithm to find the shortest path and its cost from 
        'start' to 'destination'.

        Args:
            start (int): The index of the start node.
            destination (int): The index of the destination node.

        Returns:
            tuple: A tuple containing the shortest path as a list of node indices 
            and the total cost as an integer.

        Raises:
            ValueError: If 'start' or 'destination' node index exceeds total number of nodes.
        """
        if start >= self.n_nodes or destination >= self.n_nodes:
            raise ValueError("Start or destination node index out of bounds")

        # Step 1 & 2: Initialize costs and visited nodes
        costs = [float('inf')] * self.n_nodes
        costs[start] = 0
        visited = [False] * self.n_nodes
        previous_nodes = [-1] * self.n_nodes

        # Step 3: Set previous node for each node as the start node
        previous_nodes[start] = start

        # Step 4: Create a priority queue and add the start node
        queue = [(0, start)]

        while queue:
            # Step 9: Select the unvisited node with the smallest tentative cost
            current_cost, current_node = heapq.heappop(queue)
            if visited[current_node]:
                continue

            # Step 6: Mark the current node as visited
            visited[current_node] = True

            # Step 7: Check if destination is reached
            if current_node == destination:
                break

            # Step 5: Consider nearest-neighbours of the current node
            for neighbor, edge_cost in enumerate(self.adjacency_matrix[current_node]):
                if edge_cost > 0 and not visited[neighbor]:
                    new_cost = current_cost + edge_cost
                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(queue, (new_cost, neighbor))

        # Step 8: Check if path exists
        if costs[destination] == float('inf'):
            return None, float('inf')

        # Reconstructing the path
        path = []
        node = destination
        while node != start:
            path.append(node)
            node = previous_nodes[node]
        path.append(start)
        path.reverse()

        return path, costs[destination]


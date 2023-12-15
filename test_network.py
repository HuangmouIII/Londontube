import pytest
#from network import Network
from ..londontube.network import Network #import Network according to the directory structure given in the assignment pdf

#positive tests:

#testing action of the n_nodes method
def test_network_n_nodes():
    test_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(test_adjacency_matrix)
    
    expected_n_nodes = 4
    n_nodes = test_network.n_nodes
    assert expected_n_nodes == n_nodes

#testing action of the adjacency_matrix method
def test_network_adjacency_matrix():
    input_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(input_adjacency_matrix)

    output_adjacency_matrix = test_network.adjacency_matrix
    assert input_adjacency_matrix == output_adjacency_matrix

#testing action of the Network addition method
def test_network_add():
    subnetwork_adjacency_matrix_1 = [[0, 1, 0, 0],
                                    [1, 0, 2, 0],
                                    [0, 2, 0, 0],
                                    [0, 0, 0, 0 ]]
    subnetwork_adjacency_matrix_2 = [[0, 0, 0, 3],
                                    [0, 0, 0, 1],
                                    [0, 0, 0, 0],
                                    [3, 1, 0, 0 ]]
    supernetwork_adjacency_matrix = [[0, 1, 0, 3],
                                    [1, 0, 2, 1],
                                    [0, 2, 0, 0],
                                    [3, 1, 0, 0 ]]

    subnetwork_1 = Network(subnetwork_adjacency_matrix_1)
    subnetwork_2 = Network(subnetwork_adjacency_matrix_2)
    assert (subnetwork_1 + subnetwork_2).adjacency_matrix == supernetwork_adjacency_matrix

#testing action of the distant neighbors method
@pytest.mark.parametrize("n, v, neighbors", [
    (1, 0, [1,3]), #testing nearest neighbors
    (2, 1, [0, 2, 3]), #testing second-nearest neighbors
    (3, 1, [0, 2, 3]), #testing third-nearest neighbors
])
def test_distant_neighbours(n, v, neighbors):
    test_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(test_adjacency_matrix)

    nearest_neighbours = set(test_network.distant_neighbours(n, v))
    expected_nearest_neighbors = set(neighbors)

    assert nearest_neighbours == expected_nearest_neighbors

#testing action of the dijkstra method
@pytest.mark.parametrize("test_adjacency_matrix, start, end, expected_path, expected_cost", [
    ([[0, 1, 0, 3],
      [1, 0, 2, 1],
      [0, 2, 0, 0],
      [3, 1, 0, 0 ]], 0, 2, [0, 1, 2], 3), #testing route from 0 to 2
    ([[0, 1, 0, 3],
      [1, 0, 2, 1],
      [0, 2, 0, 0],
      [3, 1, 0, 0 ]], 2, 0, [2, 1, 0], 3), #testing route from 0 to 2
    ([[0, 1, 0, 3],
      [1, 0, 0, 1],
      [0, 0, 0, 0],
      [3, 1, 0, 0 ]], 0, 2, None, float('inf')), #testing when no route exists
])
def test_dijkstra(test_adjacency_matrix, start, end, expected_path, expected_cost):
    test_network = Network(test_adjacency_matrix)

    path, cost = test_network.dijkstra(start, end)
    assert path==expected_path and cost==expected_cost

# negative tests ensuring that the errors raised while checking inputs work as expected:

#testing incorrect inputs to the Network addition method
def test_network_add_incompatible():
    test_adjacency_matrix_large = [[0, 1, 0, 3],
                                   [1, 0, 2, 1],
                                   [0, 2, 0, 0],
                                   [3, 1, 0, 0 ]]
    test_network_large = Network(test_adjacency_matrix_large)

    test_adjacency_matrix_small = [[0, 1, 0],
                                   [1, 0, 2],
                                   [0, 2, 0]]
    test_network_small = Network(test_adjacency_matrix_small)

    #the case of adding a Network to a non-Network
    with pytest.raises(TypeError, match="Both objects must be instances of Network"): 
        sum_1 = test_network_large + 1 
    
    #the case of adding Networks of different sizes
    with pytest.raises(ValueError, match="Both networks must have the same number of nodes"):
        sum_2 = test_network_large + test_network_small


#testing incorrect inputs to the adjacency_matrix property
def test_adjacency_matrix_valid():
    #the case of a non-sqaure matrix
    with pytest.raises(ValueError, match="Adjacency matrix must be square."):
        test_adjacency_matrix = [[0, 1, 0],
                                 [1, 0, 2],
                                 [0, 2, 0],
                                 [3, 1, 0]]
        test_network = Network(test_adjacency_matrix)

    #the case of a matrix with a negative entry
    with pytest.raises(ValueError, match="Adjacency matrix must have non-negative values."):
        test_adjacency_matrix = [[0, -1, 0, 3],
                                 [-1, 0, 2, 1],
                                 [0, 2, 0, 0],
                                 [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)

    #the case of an unsymmetric matrix
    with pytest.raises(ValueError, match="Adjacency matrix must be symmetric for undirected graphs."):
        test_adjacency_matrix = [[0, 2, 0, 3],
                                 [1, 0, 2, 1],
                                 [0, 2, 0, 0],
                                 [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)

#testing incorrect inputs to the distant_neighbors method
def test_distant_neighbors_input():
    with pytest.raises(ValueError, match="Node index out of bounds"):
        test_adjacency_matrix = [[0, 1, 0, 3],
                                 [1, 0, 2, 1],
                                 [0, 2, 0, 0],
                                 [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)
        nearest_neighbours = test_network.distant_neighbours(1, 4)

#testing incorrect inputs to the dijkstra method
def test_dijkstra_input():
    test_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(test_adjacency_matrix)
    
    #the case of the destination index being out of bounds
    with pytest.raises(ValueError, match="Start or destination node index out of bounds"):
        path, cost = test_network.dijkstra(0, 4)

    #the case of the start index being out of bounds
    with pytest.raises(ValueError, match="Start or destination node index out of bounds"):
        path, cost = test_network.dijkstra(4, 0)

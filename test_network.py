import pytest
from network import Network
#from ..londontube.network import Network #import Network according to the directory structure given in the assignment pdf

#positive tests:

def test_network_n_nodes():
    #test matrix taken from eqn 1 in the assignment pdf
    test_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(test_adjacency_matrix)
    
    expected_n_nodes = 4
    n_nodes = test_network.n_nodes
    assert expected_n_nodes == n_nodes

def test_network_adjacency_matrix():
    #test matrix taken from eqn 1 in the assignment pdf
    input_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(input_adjacency_matrix)

    output_adjacency_matrix = test_network.adjacency_matrix
    assert input_adjacency_matrix == output_adjacency_matrix

def test_network_add():
    #subnetwork adjacency matrix 1 and 3 from eqn 2 in the assignment pdf
    subnetwork_adjacency_matrix_1 = [[0, 1, 0, 0],
                                    [1, 0, 2, 0],
                                    [0, 2, 0, 0],
                                    [0, 0, 0, 0 ]]
    subnetwork_adjacency_matrix_2 = [[0, 0, 0, 3],
                                    [0, 0, 0, 1],
                                    [0, 0, 0, 0],
                                    [3, 1, 0, 0 ]]
    #supernetwork adjacency matrix from eqn 1 in the assignment pdf
    supernetwork_adjacency_matrix = [[0, 1, 0, 3],
                                    [1, 0, 2, 1],
                                    [0, 2, 0, 0],
                                    [3, 1, 0, 0 ]]

    subnetwork_1 = Network(subnetwork_adjacency_matrix_1)
    subnetwork_2 = Network(subnetwork_adjacency_matrix_2)
    assert (subnetwork_1 + subnetwork_2).adjacency_matrix == supernetwork_adjacency_matrix

@pytest.mark.parametrize("n, v, neighbors", [
    (1, 0, [1,3]), #testing nearest neighbors
    (2, 1, [0, 2, 3]), #testing second-nearest neighbors
    (3, 1, [0, 2, 3]), #testing third-nearest neighbors
])
def test_distant_neighbours(n, v, neighbors):
    #test matrix taken from eqn 1 in the assignment pdf
    test_adjacency_matrix = [[0, 1, 0, 3],
                             [1, 0, 2, 1],
                             [0, 2, 0, 0],
                             [3, 1, 0, 0 ]]
    test_network = Network(test_adjacency_matrix)

    nearest_neighbours = set(test_network.distant_neighbours(n, v))
    expected_nearest_neighbors = set(neighbors)

    assert nearest_neighbours == expected_nearest_neighbors

@pytest.mark.parametrize("test_adjacency_matrix, start, end, expected_path, expected_cost", [
    ([[0, 1, 0, 3],
      [1, 0, 2, 1],
      [0, 2, 0, 0],
      [3, 1, 0, 0 ]], 0, 2, [0, 1, 2], 3), #testing route from 0 to 2 (using matrix from eqn 1 in the assignment pdf)
    ([[0, 1, 0, 3],
      [1, 0, 2, 1],
      [0, 2, 0, 0],
      [3, 1, 0, 0 ]], 2, 0, [2, 1, 0], 3), #testing route from 0 to 2 (using matrix from eqn 1 in the assignment pdf)
    ([[0, 1, 0, 3],
      [1, 0, 0, 1],
      [0, 0, 0, 0],
      [3, 1, 0, 0 ]], 0, 2, None, float('inf')), #testing when no route exists (using matrix from eqn 1 in the assignment pdf with v1-v2 connection severed)
])
def test_dijkstra(test_adjacency_matrix, start, end, expected_path, expected_cost):
    #test matrix taken from eqn 1 in the assignment pdf
    test_network = Network(test_adjacency_matrix)

    path, cost = test_network.dijkstra(start, end)
    assert path==expected_path and cost==expected_cost

# negative tests ensuring that the errors raised while checking inputs work as expected:

def test_network_add_incompatible():
    #test matrix taken from eqn 1 in the assignment pdf
    test_adjacency_matrix_large = [[0, 1, 0, 3],
                              [1, 0, 2, 1],
                              [0, 2, 0, 0],
                              [3, 1, 0, 0 ]]
    test_network_large = Network(test_adjacency_matrix_large)

    test_adjacency_matrix_small = [[0, 1, 0],
                               [1, 0, 2],
                               [0, 2, 0]]
    test_network_small = Network(test_adjacency_matrix_small)

    with pytest.raises(TypeError, match="Both objects must be instances of Network"):
        sum_1 = test_network_large + 1 
    
    with pytest.raises(ValueError, match="Both networks must have the same number of nodes"):
        sum_2 = test_network_large + test_network_small

def test_adjacency_matrix_valid():
    with pytest.raises(ValueError, match="Adjacency matrix must be square."):
        test_adjacency_matrix = [[0, 1, 0],
                                 [1, 0, 2],
                                 [0, 2, 0],
                                 [3, 1, 0]]
        test_network = Network(test_adjacency_matrix)

    with pytest.raises(ValueError, match="Adjacency matrix must have non-negative values."):
        test_adjacency_matrix = [[0, -1, 0, 3],
                                 [-1, 0, 2, 1],
                                 [0, 2, 0, 0],
                                 [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)

    with pytest.raises(ValueError, match="Adjacency matrix must be symmetric for undirected graphs."):
        test_adjacency_matrix = [[0, 2, 0, 3],
                                   [1, 0, 2, 1],
                                   [0, 2, 0, 0],
                                   [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)

def test_distant_neighbors_input():
    with pytest.raises(ValueError, match="Node index out of bounds"):
        test_adjacency_matrix = [[0, 1, 0, 3],
                                 [1, 0, 2, 1],
                                 [0, 2, 0, 0],
                                 [3, 1, 0, 0 ]]
        test_network = Network(test_adjacency_matrix)
        nearest_neighbours = test_network.distant_neighbours(1, 4)

#negative test for dijkstra 
    #ValueError("Start or destination node index out of bounds")
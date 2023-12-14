import pytest
from network import Network
#from ..londontube.network import Network #import Network according to the directory structure given in the assignment pdf

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

# negative tests ensuring that the validity of inputs/raised errors work as expected:
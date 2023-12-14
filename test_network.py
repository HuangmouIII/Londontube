import pytest
from network import Network
#from ..londontube.network import Network 

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


# negative tests ensuring that the validity of inputs/raised errors work as expected:
import sys
from math import *

def generate_multiss_topology(t_networks: int, t_nodes: int, t_fail: int, nodes_count_in_mother_network: int, nodes_count_in_daughter_network: list[int]):
    if t_networks <= 0 or t_nodes <= 0 or t_fail <= 0 or nodes_count_in_mother_network <= 0 or any(nodes <= 0 for nodes in nodes_count_in_daughter_network):
        raise Exception("All numbers must be strictly positive integers")
    if t_networks > len(nodes_count_in_daughter_network) + 1:
        raise Exception("t_networks is greater than the total number of networks")
    total_nodes_number = sum(nodes_count_in_daughter_network) + nodes_count_in_mother_network
    if t_nodes > total_nodes_number:
        raise Exception("t_nodes is greater than the total number of nodes")
    if t_fail > nodes_count_in_mother_network:
        raise Exception("t_fail is greater than the number of nodes in mother network")
    threshold_P = nodes_count_in_mother_network - t_fail + 1
    num_polynomial_Q = nodes_count_in_mother_network
    threshold_Q = t_networks

    print("Generate a polynomial P of degree", threshold_P - 1, "such that secret = P(0)")
    print("Generate", num_polynomial_Q, "polynomials", ", ".join(["Q"+str(i) for i in range(1, num_polynomial_Q + 1)]), "of degree", threshold_Q - 1, "such that",
          ", ".join(["Q"+str(i)+"(0) = P(" + str(i) + ")" for i in range(1, num_polynomial_Q + 1)]))
    print("In mother network, distribute", ", ".join(["Q"+str(i)+"(1) to node " + str(i) for i in range(1, num_polynomial_Q + 1)]))

    for i in range(1, num_polynomial_Q + 1):
        print("Generate", ", ".join(["Q'" + str(i) +"(" + str(j) + ")" for j in range(1, len(nodes_count_in_daughter_network) + 1)]))

    threshold_R = (t_nodes - threshold_P) / (threshold_Q - 1) # Here we assume each daughter subnetworks have roughly the same number of nodes, to simplify
    if not threshold_R.is_integer():
        print("WARNING: t_nodes won't be accurate due to given configuration incompatibility, keeping the most secure option")
    threshold_R = ceil(threshold_R)
    if len([nodes_count for nodes_count in nodes_count_in_daughter_network if nodes_count >= threshold_R]) < threshold_Q - 1:
        raise Exception("Error: cannot generate a valid topology for the given parameters. Try to lower some thresholds or raise node count in daughter networks")
    num_polynomial_R = 1
    for daughter_network in range(1, len(nodes_count_in_daughter_network) + 1):
        for num_polynomial_Q in range(1, num_polynomial_Q + 1):
            print("Generate polynomial R" + str(num_polynomial_R), "of degree", threshold_R - 1, "such that R" + str(num_polynomial_R) + "(0) = Q'" + str(num_polynomial_Q)
                  + "(" + str(daughter_network) + ") and distribute it over daughter network", daughter_network)
            num_polynomial_R += 1


print("TEST 1")
generate_multiss_topology(3, 6, 2, 3, [3, 3, 3])

print("\n\n")
print("TEST 2")
generate_multiss_topology(3, 5, 2, 2, [3, 3, 3])

print("\n\n")
print("TEST 3")
generate_multiss_topology(4, 5, 2, 2, [3, 3, 3])

print("\n\n")
print("TEST 4")
generate_multiss_topology(3, 6, 2, 3, [3, 3])
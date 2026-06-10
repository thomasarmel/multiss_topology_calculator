import itertools


def generate_multiss_topology_standard(t_networks: int, t_nodes: int, t_fail: int, nodes_count_in_mother_network: int, nodes_count_in_daughter_network: list[int]):
    l = len(nodes_count_in_daughter_network) + 1
    n_0 = nodes_count_in_mother_network
    n_daughters = nodes_count_in_daughter_network

    T_P = t_networks

    print(f"Target:")
    print(f" - t_networks: {t_networks}")
    print(f" - t_nodes: {t_nodes}")
    print(f" - t_fail: {t_fail}")
    print("--------------------------------------")

    if T_P > l:
        print("Error: t_networks cannot be strictly greater than the total number of networks (l).")
        return

    ranges = [range(1, n_0 + 1)] + [range(1, n + 1) for n in n_daughters]

    valid_config = None

    for combo in itertools.product(*ranges):
        T_Q0 = combo[0]
        T_Q_daughters = combo[1:]

        sorted_T_Q = sorted(T_Q_daughters)
        calculated_t_nodes = T_Q0 + sum(sorted_T_Q[:T_P - 1])

        tf0 = n_0 - T_Q0 + 1

        daughter_fail_vals = [n_i - t_qi + 1 for n_i, t_qi in zip(n_daughters, T_Q_daughters)]
        sorted_fail_vals = sorted(daughter_fail_vals)
        tf1 = sum(sorted_fail_vals[:l - T_P + 1])

        calculated_t_fail = min(tf0, tf1)

        # Check if constraints are perfectly met
        if calculated_t_nodes == t_nodes and calculated_t_fail == t_fail:
            valid_config = combo
            break

    if not valid_config:
        print("Error: No valid polynomial degrees found for the given thresholds.")
        return

    T_Q0 = valid_config[0]
    T_Q_daughters = valid_config[1:]

    # Display the final polynomials and distributions
    print(f" - Polynomial P threshold: {T_P}")
    print("--------------------------------------")

    print("Mother Network N_0:")
    print(f" - Nodes count: {n_0}")
    print(f" - Polynomial Q_0 threshold: {T_Q0}")
    print(f" - Relation: Q_0(0) = P(1)")
    print(f" - Distribution: Evaluations Q_0(1) to Q_0({n_0}) are stored in nodes 1 to {n_0}.")
    print("--------------------------------------")

    for i, (n_i, T_Qi) in enumerate(zip(n_daughters, T_Q_daughters), start=1):
        print(f"Daughter Network N_{i}:")
        print(f" - Nodes count: {n_i}")
        print(f" - Polynomial Q_{i} threshold: {T_Qi}")
        print(f" - Relation: Q_{i}(0) = P'({i + 1})")
        print(f" - Distribution: Evaluations Q_{i}(1) to Q_{i}({n_i}) are stored in nodes 1 to {n_i}.")


def generate_multiss_topology_local(t_networks: int, t_nodes: int, t_fail: int, nodes_count_in_mother_network: int, nodes_count_in_daughter_network: list[int]):
    assert len(nodes_count_in_daughter_network) == nodes_count_in_mother_network, "Error: Local mode requires the number of daughter subnets to strictly equal the number of nodes in the mother subnet."

    l = len(nodes_count_in_daughter_network) + 1
    n_0 = nodes_count_in_mother_network
    n_daughters = nodes_count_in_daughter_network

    T_P = t_networks - 1

    print(f"Target:")
    print(f" - t_networks: {t_networks}")
    print(f" - t_nodes: {t_nodes}")
    print(f" - t_fail: {t_fail}")
    print("--------------------------------------")

    if T_P <= 0 or T_P >= l:
        print("Error: Invalid t_networks for the current topology.")
        return

    expected_t_fail = n_0 - T_P + 1
    if t_fail != expected_t_fail:
        print(f"Error: Constraints mismatch. For local mode, t_fail is fixed to n_0 - T(P) + 1 = {expected_t_fail}.")
        return

    ranges = [range(1, n + 1) for n in n_daughters]

    valid_config = None

    for combo in itertools.product(*ranges):
        T_R_daughters = combo

        sorted_T_R = sorted(T_R_daughters)
        calculated_t_nodes = T_P + sum(sorted_T_R[:T_P])

        if calculated_t_nodes == t_nodes:
            valid_config = combo
            break

    if not valid_config:
        print("Error: No valid polynomial degrees found for the given thresholds.")
        return

    T_R_daughters = valid_config

    print(f" - Polynomial P threshold: {T_P}")
    print("--------------------------------------")

    print("Mother Network N_0:")
    print(f" - Nodes count: {n_0}")
    print(f" - Distribution: For each node i in 1 to {n_0}:")
    print(f"     Node i stores Q_i(1)")
    print(f"     Where Q_i is degree 1, and Q_i(0) = P(i)")
    print("--------------------------------------")

    for i, (n_i, T_Ri) in enumerate(zip(n_daughters, T_R_daughters), start=1):
        print(f"Daughter Network N_{i}:")
        print(f" - Nodes count: {n_i}")
        print(f" - Polynomial R_{i} threshold: {T_Ri}")
        print(f" - Relation: R_{i}(0) = Q'_{i}(2)")
        print(f" - Distribution: Evaluations R_{i}(1) to R_{i}({n_i}) are stored in nodes 1 to {n_i}.")


print("STANDARD:")

print("TEST 1")
generate_multiss_topology_standard(3, 6, 2, 3, [3, 3, 3])

print("\n\n")
print("TEST 2")
generate_multiss_topology_standard(3, 5, 2, 2, [3, 3, 3])

print("\n\n")
print("TEST 3")
generate_multiss_topology_standard(4, 5, 2, 2, [3, 3, 3])

print("\n\n")
print("TEST 4")
generate_multiss_topology_standard(3, 6, 2, 3, [3, 3])


print("LOCAL:")

print("TEST 1")
generate_multiss_topology_local(3, 6, 2, 3, [3, 3, 3])
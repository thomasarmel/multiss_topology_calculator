# MULTISS topology calculator

Generate standard-mode MULTISS polynomial share configuration for a given network topology and configured thresholds:
- t_nodes: minimum number of nodes to reconstruct the secret
- t_networks: minimum number of QKD subnets to use to reconstruct the secret
- t_fail: minimum number of nodes to shut down to make the secret unavailable

### Usage

```python
generate_multiss_topology(t_networks: int, t_nodes: int, t_fail: int, nodes_in_mother_network: int, nodes_count_in_daughter_network: list[int])
```

Print the polynomial share configuration in the console.
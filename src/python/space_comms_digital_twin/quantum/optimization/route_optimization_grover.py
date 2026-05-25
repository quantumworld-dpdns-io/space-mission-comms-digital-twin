from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from space_comms_digital_twin.quantum.optimization.grover_search import (
    GroverResult,
    GroverSearch,
)


@dataclass
class RouteProblem:
    n_nodes: int = 0
    adjacency: np.ndarray = field(default_factory=lambda: np.zeros((1, 1)))
    source: int = 0
    target: int = 0
    max_hops: int = 3


class RouteOptimizationGrover:
    def __init__(self, n_qubits: int = 4):
        self.n_qubits = n_qubits
        self.grover = GroverSearch(n_qubits=n_qubits)

    def build_problem(self, n_nodes: int, edges: list[tuple[int, int, float]],
                      source: int, target: int,
                      max_hops: int = 3) -> RouteProblem:
        adj = np.full((n_nodes, n_nodes), float('inf'))
        for u, v, w in edges:
            adj[u, v] = w
            adj[v, u] = w
        np.fill_diagonal(adj, 0)

        return RouteProblem(
            n_nodes=n_nodes,
            adjacency=adj,
            source=source,
            target=target,
            max_hops=max_hops,
        )

    def _encode_path(self, path: list[int], n_nodes: int) -> int:
        encoding = 0
        for node in path:
            encoding = (encoding << (n_nodes.bit_length())) | node
        return encoding

    def _decode_path(self, encoded: int, n_nodes: int, hops: int) -> list[int]:
        path = []
        bits = n_nodes.bit_length() or 1
        mask = (1 << bits) - 1
        for _ in range(hops):
            node = encoded & mask
            path.append(node)
            encoded >>= bits
        return list(reversed(path))

    def solve(self, problem: RouteProblem) -> GroverResult:
        min(self.n_qubits, 4)

        def predicate(state: int) -> bool:
            path = self._decode_path(state, problem.n_nodes, 2)
            if not path:
                return False
            cost = 0
            for i in range(len(path) - 1):
                if problem.adjacency[path[i], path[i + 1]] == float('inf'):
                    return False
                cost += problem.adjacency[path[i], path[i + 1]]
            return path[0] == problem.source and path[-1] == problem.target

        O = self.grover.phase_oracle(predicate)
        result = self.grover.search(O)
        return result

    def compare_with_classical(self, problem: RouteProblem) -> dict[str, float]:
        quantum_result = self.solve(problem).success_probability
        return {
            "quantum_success_probability": quantum_result,
            "classical_optimal_cost": float(np.min(problem.adjacency)),
        }

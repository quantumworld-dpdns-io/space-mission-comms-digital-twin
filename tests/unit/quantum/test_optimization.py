import pytest
import numpy as np
from space_comms_digital_twin.quantum.optimization.qaoa import QAOA
from space_comms_digital_twin.quantum.optimization.vqe import VQE
from space_comms_digital_twin.quantum.optimization.grover_search import GroverSearch


def test_qaoa_hamiltonian():
    qaoa = QAOA(n_layers=1)
    edges = [(0, 1), (1, 2)]
    H = qaoa.build_maxcut_hamiltonian(edges, 3)
    assert H.shape == (8, 8)


def test_qaoa_solve():
    qaoa = QAOA(n_layers=1)
    edges = [(0, 1)]
    H = qaoa.build_maxcut_hamiltonian(edges, 2)
    result = qaoa.solve(H, max_iterations=10)
    assert result.optimal_value != 0


def test_vqe_hamiltonian():
    vqe = VQE(n_qubits=2)
    pauli = [("ZZ", -1.0), ("II", 0.5)]
    H = vqe.build_hamiltonian(pauli)
    assert H.shape == (4, 4)


def test_vqe_solve():
    vqe = VQE(n_qubits=2, n_layers=1)
    pauli = [("ZZ", -1.0)]
    H = vqe.build_hamiltonian(pauli)
    result = vqe.solve(H, max_iterations=10)
    assert result.optimal_energy < 0


def test_grover_search():
    grover = GroverSearch(n_qubits=3)
    O = grover.oracle(5)
    result = grover.search(O)
    assert result.found_solution is not None


def test_grover_optimal_iterations():
    grover = GroverSearch(n_qubits=10)
    n = grover.optimal_iteration_count()
    assert n > 0

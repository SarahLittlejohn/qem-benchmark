"""Kicked Ising circuit benchmark: tests mitigation on a realistic workload."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector

MAX_EXACT_QUBITS = 20


def build(n: int, depth: int = 1, theta: float = np.pi / 4) -> tuple[QuantumCircuit, SparsePauliOp, float]:
    """Build an n-qubit kicked Ising circuit with `depth` Trotter steps.

    Each step applies RX(theta) to every qubit (the "kick"), then RZZ(-pi/2)
    between every pair of neighbouring qubits. Returns the circuit, the
    average-Z observable (magnetisation) and its ideal value, calculated
    exactly with a statevector simulation.
    """
    if n < 2:
        raise ValueError("An Ising chain needs at least 2 qubits")
    if depth < 1:
        raise ValueError("Depth must be at least 1")
    if n > MAX_EXACT_QUBITS:
        raise ValueError(f"Exact ideal values are only calculated up to {MAX_EXACT_QUBITS} qubits")

    qc = QuantumCircuit(n, name=f"ising_{n}_d{depth}")
    for _ in range(depth):
        # Kick: rotate every qubit by theta around X
        for q in range(n):
            qc.rx(theta, q)
        # Interaction: RZZ on even pairs (0-1, 2-3, ...), then odd pairs (1-2, 3-4, ...)
        for start in (0, 1):
            for q in range(start, n - 1, 2):
                qc.rzz(-np.pi / 2, q, q + 1)

    # Average magnetisation: the average of Z on each qubit
    observable = SparsePauliOp.from_sparse_list(
        [("Z", [q], 1 / n) for q in range(n)], num_qubits=n
    )

    # Ideal value from an exact (noiseless) simulation
    ideal = float(Statevector(qc).expectation_value(observable).real)
    return qc, observable, ideal
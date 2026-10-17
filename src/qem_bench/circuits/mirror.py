"""Mirror circuit benchmark: tests how mitigation scales with depth."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp


def build(n: int, depth: int = 1, seed: int = 0) -> tuple[QuantumCircuit, SparsePauliOp, float]:
    """Build an n-qubit mirror circuit: random layers U, then U inverse.

    Returns the circuit, the average-Z observable and its ideal
    expectation value (1.0), since the circuit returns |00...0>.
    """
    if n < 2:
        raise ValueError("A mirror circuit needs at least 2 qubits")
    if depth < 1:
        raise ValueError("Depth must be at least 1")

    rng = np.random.default_rng(seed)

    # U: each layer has random single-qubit rotations, then a brickwork of CNOTs
    u = QuantumCircuit(n)
    for layer in range(depth):
        for q in range(n):
            u.u(*rng.uniform(0, 2 * np.pi, size=3), q)
        for q in range(layer % 2, n - 1, 2):
            u.cx(q, q + 1)

    # Mirror: U, a barrier so the transpiler print(backend.target["cz"])can't cancel them, then U inverse
    qc = QuantumCircuit(n, name=f"mirror_{n}_d{depth}")
    qc.compose(u, inplace=True)
    qc.barrier()
    qc.compose(u.inverse(), inplace=True)

    # Average of Z on each qubit, which is 1 for |00...0>
    observable = SparsePauliOp.from_sparse_list(
        [("Z", [q], 1 / n) for q in range(n)], num_qubits=n
    )
    return qc, observable, 1.0
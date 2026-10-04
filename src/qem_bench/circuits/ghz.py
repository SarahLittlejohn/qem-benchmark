from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

def build(n: int, depth: int = 0) -> tuple[QuantumCircuit, SparsePauliOp, float]:
    """Build an n-qubit GHZ circuit.
 
    Returns the circuit, the observable X⊗X⊗...⊗X and its ideal
    expectation value (1.0). `depth` is unused here but keeps the
    interface the same across all circuit modules.
    """

    # Number of qubits must be at least 2 for a GHZ state
    if n < 2:
        raise ValueError("A GHZ state needs at least 2 qubits")

    # Build the GHZ circuit, all qubits start in the |0> state
    qc = QuantumCircuit(n, name=f"ghz_{n}")
    # Applies a Hadamard to qubit 0, turning it into (|0⟩ + |1⟩)/√2. The others are still |0⟩.
    qc.h(0)
    # range(n - 1) gives 0, 1, …, n−2
    for i in range(n - 1):
        # Each CNOT flips its target if its control is 1, so the "0 or 1" of qubit 0 spreads down the chain.
        qc.cx(i, i + 1)

    # The observable we are interested in is X⊗X⊗...⊗X
    observable = SparsePauliOp("X" * n)

    # The ideal expectation value of this observable for the GHZ state is 1.0
    return qc, observable, 1.0

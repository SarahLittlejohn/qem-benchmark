import time

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator


def run(circuit, observable, backend, shots=4096, seed=42):
    # generate_preset_pass_manager(...) creates a "pass manager": 
    # a pipeline of steps (passes) that rewrites your circuit for the device. 
    # It reads the backend's gates and connectivity to know what to aim for. optimization_level=1 does light optimisation; levels go from 0 (none) to 3 (heaviest).
    pm = generate_preset_pass_manager(
        backend=backend, optimization_level=1, seed_transpiler=seed
    )
    # Apply the pass manager to the circuit to get an ISA-compliant circuit
    isa_circuit = pm.run(circuit)
    # The transpiler always produces a circuit as wide as the device, so for Fez that's 156 qubits.
    # Remaps remaps the observable so it acts on the same physical qubits the circuit ended up on.
    isa_observable = observable.apply_layout(isa_circuit.layout)

    # Runtime Estimator: samples the ISA circuit on the backend (noise included) and returns the observable's expectation value
    estimator = Estimator(mode=backend)
    estimator.options.default_shots = shots
    # This is the built in error mitigation
    estimator.options.resilience_level = 0

    # Run and time it
    start = time.perf_counter()
    result = estimator.run([(isa_circuit, isa_observable)]).result()
    runtime = time.perf_counter() - start

    # Primitive Unified Bloc: the bundle of inputs for one task you hand to a primitive (one of the standard operations for getting results out of a quantum computer)
    pub = result[0]
    return {
        "estimate": float(pub.data.evs),
        "std": float(pub.data.stds),
        "shots": shots,
        "circuits": 1,
        "runtime_s": runtime,
    }
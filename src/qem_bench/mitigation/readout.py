"""Readout error mitigation with mthree: corrects for qubits being misread at measurement."""

import time

import mthree
import numpy as np
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


def _measurement_basis(observable):
    """Work out which basis to measure each qubit in, e.g. X for GHZ, Z for mirror and Ising."""
    basis = ["I"] * observable.num_qubits
    for pauli in observable.paulis:
        for q in range(observable.num_qubits):
            p = str(pauli[q])
            if p == "I":
                continue
            if basis[q] not in ("I", p):
                raise ValueError("Observable needs more than one measurement basis on a qubit")
            basis[q] = p
    return basis


def _value_per_bitstring(observable, bitstring):
    """The observable's value for one measured bitstring, e.g. +1 or -1 for X⊗X⊗X."""
    bits = bitstring[::-1]  # Qiskit bitstrings are written right to left: qubit 0 is last
    total = 0.0
    for pauli, coeff in zip(observable.paulis, observable.coeffs):
        sign = 1
        for q in range(observable.num_qubits):
            if str(pauli[q]) != "I" and bits[q] == "1":
                sign = -sign
        total += coeff.real * sign
    return total


def run(circuit, observable, backend, shots=4096, seed=42):
    # Rotate each qubit so its measurement basis becomes Z, then measure everything
    measured = circuit.copy()
    for q, b in enumerate(_measurement_basis(observable)):
        if b == "X":
            measured.h(q)
        elif b == "Y":
            measured.sdg(q)
            measured.h(q)
    measured.measure_all()

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1, seed_transpiler=seed)
    isa_circuit = pm.run(measured)
    # Which physical qubit each measurement came from, so the right calibration is used
    mapping = mthree.utils.final_measurement_mapping(isa_circuit)

    start = time.perf_counter()

    # Run the circuit and get raw counts, e.g. {"0110": 512, ...}
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = shots
    counts = sampler.run([isa_circuit]).result()[0].data.meas.get_counts()

    # Calibrate: measure all-0 and all-1 states to learn how often each qubit is misread
    mit = mthree.M3Mitigation(backend)
    mit.cals_from_system(mapping, shots=shots, method="independent")

    # Correct the counts into a quasi-probability distribution
    quasi = mit.apply_correction(counts, mapping, return_mitigation_overhead=True)

    runtime = time.perf_counter() - start

    # Expectation value: average of the observable's value over the corrected distribution
    values = {b: _value_per_bitstring(observable, b) for b in quasi}
    estimate = sum(p * values[b] for b, p in quasi.items())
    second_moment = sum(p * values[b] ** 2 for b, p in quasi.items())
    std = np.sqrt(max(second_moment - estimate**2, 0) * quasi.mitigation_overhead / shots)

    return {
        "estimate": float(estimate),
        "std": float(std),
        "shots": 3 * shots,  # the circuit plus two calibration circuits
        "circuits": 3,
        "runtime_s": runtime,
    }
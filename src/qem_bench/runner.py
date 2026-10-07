
""" Runs a complete experiment. For a chosen circuit, it loops over each mitigation 
    technique and each circuit size, builds the circuit, runs it, records everything 
    about that run as a row, then saves all the rows via results.py"""

import importlib
# Lets you import a module from its name as a string.
from datetime import datetime, timezone
# Lets you get the current date and time in UTC and format it

from qem_bench import results
from qem_bench.backends import get_backend
# Imports modules: saving results and getting the backend.

def run_experiment(name, circuit, techniques, sizes, backend_name="fake_fez", shots=4096, depth=0):
    # Import modules by name, e.g. "ghz" -> qem_bench.circuits.ghz
    circuit_module = importlib.import_module(f"qem_bench.circuits.{circuit}")
    # Turns "ghz" into the actual qem_bench.circuits.ghz module
    backend = get_backend(backend_name)
    # Gets the backend object based on the backend name.

    rows = []
    # An empty list to collect one dictionary per run.
    for technique in techniques:
        technique_module = importlib.import_module(f"qem_bench.mitigation.{technique}")
        # Turns "none" into the actual qem_bench.mitigation.none module (etc.)

        for n in sizes:
            # Loops over each circuit size.
            qc, observable, ideal = circuit_module.build(n, depth)
            # Builds the circuit and unpacks the three things it returns.
            output = technique_module.run(qc, observable, backend, shots=shots)
            # Runs the mitigation technique on the circuit and gets the dictionay output (estimate, std, shots, circuits, runtime_s).

            rows.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "circuit": circuit,
                "n": n,
                "depth": depth,
                "technique": technique,
                "backend": backend_name,
                "ideal": ideal,
                "abs_error": abs(output["estimate"] - ideal),
                **output,  # estimate, std, shots, circuits, runtime_s
            })
            # Adds one row describing the run.
            print(f"{circuit} n={n} {technique}: {output['estimate']:.3f}")
            # Shows progress as it runs.

    return results.save(rows, name)
    # After all loops finish, saves everything in one go and returns the file path.


if __name__ == "__main__":
    path = run_experiment("ghz_baseline", circuit="ghz", techniques=["none"], sizes=[2, 4, 6, 8, 10, 12])
    print(f"Saved to {path}")
# This block only runs when you execute the file directly (python -m qem_bench.runner), 
# not when another file imports it. It's the standard way to give a module a "run me" entry point.
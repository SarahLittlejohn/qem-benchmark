import pytest
# A perfect, noiseless simulator that calculates expectation values exactly using the full quantum state.
from qiskit.primitives import StatevectorEstimator

from qem_bench.circuits import ghz

@pytest.mark.parametrize("n", [2, 3, 5, 8])
def test_ghz_ideal_value(n):
    qc, observable, ideal = ghz.build(n)
    # Creates the simulator and runs it.
    result = StatevectorEstimator().run([(qc, observable)]).result()
    # Extract the expectation value from the result.
    assert float(result[0].data.evs) == pytest.approx(ideal)
 
 
def test_ghz_rejects_single_qubit():
    with pytest.raises(ValueError):
        ghz.build(1)




"""Check each benchmark circuit returns its ideal value with no noise."""

import pytest
from qiskit.primitives import StatevectorEstimator

from qem_bench.circuits import ghz, mirror


# --- GHZ ---

@pytest.mark.parametrize("n", [2, 3, 5, 8])
def test_ghz_ideal_value(n):
    qc, observable, ideal = ghz.build(n)
    result = StatevectorEstimator().run([(qc, observable)]).result()
    assert float(result[0].data.evs) == pytest.approx(ideal)


def test_ghz_rejects_single_qubit():
    with pytest.raises(ValueError):
        ghz.build(1)


# --- Mirror ---

@pytest.mark.parametrize("n, depth", [(2, 1), (3, 2), (5, 4), (8, 6)])
def test_mirror_ideal_value(n, depth):
    qc, observable, ideal = mirror.build(n, depth)
    result = StatevectorEstimator().run([(qc, observable)]).result()
    assert float(result[0].data.evs) == pytest.approx(ideal)


def test_mirror_same_seed_gives_same_circuit():
    assert mirror.build(4, 3, seed=1)[0] == mirror.build(4, 3, seed=1)[0]


def test_mirror_different_seeds_give_different_circuits():
    assert mirror.build(4, 3, seed=1)[0] != mirror.build(4, 3, seed=2)[0]


@pytest.mark.parametrize("n, depth", [(1, 1), (3, 0)])
def test_mirror_rejects_bad_input(n, depth):
    with pytest.raises(ValueError):
        mirror.build(n, depth)
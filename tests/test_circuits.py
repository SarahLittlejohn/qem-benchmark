"""Check each benchmark circuit returns its ideal value with no noise."""

import pytest
from qiskit.primitives import StatevectorEstimator

from qem_bench.circuits import ghz, ising, mirror


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


# --- Ising ---

@pytest.mark.parametrize("n, depth", [(2, 1), (4, 2), (6, 4)])
def test_ising_ideal_matches_estimator(n, depth):
    qc, observable, ideal = ising.build(n, depth)
    result = StatevectorEstimator().run([(qc, observable)]).result()
    assert float(result[0].data.evs) == pytest.approx(ideal)


def test_ising_with_no_kick_stays_at_one():
    # With theta = 0, the RZZ gates only add phases, so every qubit stays in |0>
    _, _, ideal = ising.build(4, 3, theta=0)
    assert ideal == pytest.approx(1.0)


def test_ising_ideal_is_non_trivial():
    _, _, ideal = ising.build(4, 2)
    assert -1 < ideal < 1


@pytest.mark.parametrize("n, depth", [(1, 1), (3, 0), (21, 1)])
def test_ising_rejects_bad_input(n, depth):
    with pytest.raises(ValueError):
        ising.build(n, depth)
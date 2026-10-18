"""Check the readout module's helper functions (fast: no simulation needed)."""

import pytest

from qem_bench.circuits import ghz, mirror
from qem_bench.mitigation.readout import _measurement_basis, _value_per_bitstring


def test_ghz_is_measured_in_x_basis():
    _, observable, _ = ghz.build(4)
    assert _measurement_basis(observable) == ["X", "X", "X", "X"]


def test_mirror_is_measured_in_z_basis():
    _, observable, _ = mirror.build(4, 2)
    assert _measurement_basis(observable) == ["Z", "Z", "Z", "Z"]


@pytest.mark.parametrize("bitstring, expected", [
    ("0000", 1),   # |++++>: no -1s, product +1
    ("0110", 1),   # |+--+>: two -1s, product +1
    ("0010", -1),  # one -1: product -1 (an error)
])
def test_ghz_value_is_product_of_signs(bitstring, expected):
    _, observable, _ = ghz.build(4)
    assert _value_per_bitstring(observable, bitstring) == pytest.approx(expected)


def test_mirror_value_is_average_of_signs():
    _, observable, _ = mirror.build(4, 2)
    # Qubit 0 read as 1 (rightmost character), the rest as 0: (-1 + 1 + 1 + 1) / 4
    assert _value_per_bitstring(observable, "0001") == pytest.approx(0.5)
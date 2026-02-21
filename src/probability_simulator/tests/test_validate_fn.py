"""Testing validation functions"""

import pytest
from probability_simulator.utility import is_callable, in_inclusive_range


@pytest.mark.parametrize(
    "inputfn, exp",
    [(lambda x: 1, True), (lambda x, y: None, True), (1, False), ("str", False)],
)
def test_is_callable(inputfn, exp):
    assert is_callable(inputfn) is exp

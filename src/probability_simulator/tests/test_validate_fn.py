"""Testing validation functions"""

import pytest
from probability_simulator.utility import is_callable, in_inclusive_range


@pytest.mark.parametrize(
    "inputfn, exp",
    [(lambda x: 1, True), (lambda x, y: None, True), (1, False), ("str", False)],
)
def test_is_callable(inputfn, exp):
    assert is_callable(inputfn) is exp


@pytest.mark.parametrize(
    "n, minc, maxc, exp", [
        (1,1,1,True),
        (1,2,3, False),
        (1,2,-1, False),
        (1, -1, 1, True),
        (1, 0, 10, True),
        (1, None, 10, True),
        (1, None, -1 , False),
        (1, 0, None, True), 
        (1, 2, None, False)
    ]
)
def test_in_inclusive_range(n, minc, maxc, exp):
    assert in_inclusive_range(n,minc,maxc) == exp
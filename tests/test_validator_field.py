import pytest
import math
from probability_simulator.validation import RealNumber

# tests/test_field_realnumber.py

from probability_simulator.validation import Field


# Tests for Field with allow_none
@pytest.mark.parametrize(
    "expected_type, value, allow_none, should_raise",
    [
        (int, None, True, False),  # None allowed → no error
        (int, None, False, True),  # None not allowed → raises TypeError
        (int, 42, False, False),  # valid type → no error
        (
            None,
            None,
            False,
            False,
        ),  # None is a valid type of None -> no error
        (None, None, True, False),  # None is a valid type of None -> no error
    ],
)
def test_field_allow_none(expected_type, value, allow_none, should_raise):
    class Example:
        x = Field(expected_type=expected_type, allow_none=allow_none)

    e = Example()
    if should_raise:
        with pytest.raises(TypeError):
            e.x = value
    else:
        e.x = value
        assert e.x == value


@pytest.fixture
def example_realnumber_autoconvert():
    class Example:
        y = RealNumber(auto_convert=True)

    return Example


# ------------------------------
# RealNumber Tests
# ------------------------------


@pytest.mark.parametrize(
    "value,expected",
    [
        (1.5, 1.5),
        ("2.7", 2.7),
        (" +inf ", float("inf")),
        ("-INFINITY", float("-inf")),
        ("-infinity", float("-inf")),
        (3, 3),
        ("abc", "abc"),
        (" - inf", -1 * math.inf),
        ("j", "j"),
        (3, 3),
        (2.0, 2.0),
        ("2. 00", 2),
        (" jjjj ", " jjjj "),
    ],
)
def test_realnumber_preprocess_and_assignment(value, expected):
    value = RealNumber.preprocess_str_to_real(value, None)
    if isinstance(value, float):
        assert math.isclose(value, expected, rel_tol=1e-12)
    else:
        assert value == expected


# test that realnumber

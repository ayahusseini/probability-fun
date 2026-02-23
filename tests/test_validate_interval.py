"""Tests on the Interval object"""

import pytest
import numbers
from probability_simulator.validation.interval import IntervalBracket, Interval


def test_enum_members():
    """Check that all enum members exist and have correct values"""
    assert IntervalBracket.left_open.value == "("
    assert IntervalBracket.left_closed.value == "["
    assert IntervalBracket.right_open.value == ")"
    assert IntervalBracket.right_closed.value == "]"


@pytest.mark.parametrize(
    "bracket, expected_is_left, expected_is_right, expected_is_open, expected_is_closed",
    [
        (IntervalBracket.left_open, True, False, True, False),
        (IntervalBracket.left_closed, True, False, False, True),
        (IntervalBracket.right_open, False, True, True, False),
        (IntervalBracket.right_closed, False, True, False, True),
    ],
)
def test_bracket_properties(
    bracket,
    expected_is_left,
    expected_is_right,
    expected_is_open,
    expected_is_closed,
):
    """Test the boolean properties of IntervalBracket"""
    assert bracket.is_left == expected_is_left
    assert bracket.is_right == expected_is_right
    assert bracket.is_open == expected_is_open
    assert bracket.is_closed == expected_is_closed


def test_enum_uniqueness():
    """Check that all enum values are unique"""
    values = [member.value for member in IntervalBracket]
    assert len(values) == len(set(values))


def test_enum_iteration():
    """Check that iteration returns all members"""
    members = list(IntervalBracket)
    assert IntervalBracket.left_open in members
    assert IntervalBracket.left_closed in members
    assert IntervalBracket.right_open in members
    assert IntervalBracket.right_closed in members


@pytest.mark.parametrize(
    "interval_str, expected",
    [
        ("[1,2]", ("[", "1", "2", "]")),
        ("(0, 1)", ("(", "0", "1", ")")),
        ("  [  -5 ,  10  )  ", ("[", "-5", "10", ")")),
        ("(3.14, 2.71]", ("(", "3.14", "2.71", "]")),
        ("[-inf, inf)", ("[", "-inf", "inf", ")")),
        ("\t( 0 , 100 ]\n", ("(", "0", "100", "]")),
    ],
)
def test_extract_pattern_components_valid(interval_str, expected):
    left, lower, upper, right = Interval.extract_pattern_components(
        interval_str
    )
    assert (left, lower, upper, right) == expected


@pytest.mark.parametrize(
    "invalid_str",
    [
        "",  # empty string
        "1,2",  # missing brackets
        "[1 2]",  # missing comma
        "[1,2",  # missing closing bracket
        "1,2]",  # missing opening bracket
        "[,]",  # empty bounds
        None,  # non-string input
        123,  # non-string input
    ],
)
def test_extract_pattern_components_invalid(invalid_str):
    if isinstance(invalid_str, str):
        # string but invalid → ValueError
        with pytest.raises(ValueError):
            Interval.extract_pattern_components(invalid_str)
    else:
        # non-string → validate_type should raise TypeError
        with pytest.raises(TypeError):
            Interval.extract_pattern_components(invalid_str)


@pytest.mark.parametrize(
    "interval_str, expected",
    [
        ("[1,2]", ("[", "1", "2", "]")),
        (" [1,2]", ("[", "1", "2", "]")),
        ("[1,2] ", ("[", "1", "2", "]")),
        ("   [ 1 , 2 ]   ", ("[", "1", "2", "]")),
        ("\t[1,2]\n", ("[", "1", "2", "]")),
    ],
)
def test_extract_pattern_components_whitespace(interval_str, expected):
    left, lower, upper, right = Interval.extract_pattern_components(
        interval_str
    )
    assert (left, lower, upper, right) == expected


@pytest.mark.parametrize(
    "interval_str, test_value, expected",
    [
        # closed intervals
        ("[0,1]", 0, True),
        ("[0,1]", 0.5, True),
        ("[0,1]", 1, True),
        ("[0,1]", -0.1, False),
        ("[0,1]", 1.1, False),
        # open intervals
        ("(0,1)", 0, False),
        ("(0,1)", 0.5, True),
        ("(0,1)", 1, False),
        # mixed intervals
        ("[0,1)", 0, True),
        ("[0,1)", 1, False),
        ("(0,1]", 0, False),
        ("(0,1]", 1, True),
        # infinite bounds
        ("(-inf, 0]", -1e10, True),
        ("(-inf, 0]", 0, True),
        ("(-inf, 0]", 1, False),
        ("[0, inf)", 0, True),
        ("[0, inf)", 1e10, True),
        ("[0, inf)", -1, False),
        # float/int mix
        ("[0,2.5]", 2.5, True),
        ("[0,2.5]", 2, True),
        ("[0,2.5]", 0, True),
    ],
)
def test_interval_contains(interval_str, test_value, expected):
    interval = Interval(interval_str)
    assert isinstance(interval.lower, numbers.Real)
    assert isinstance(interval.lower, numbers.Real)
    assert (test_value in interval) == expected

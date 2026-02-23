import pytest
from probability_simulator.validation import RealNumberWithinInterval

# ----------------------------
# Basic interval validation
# ----------------------------


@pytest.mark.parametrize(
    "interval_str, value, should_pass",
    [
        # Closed intervals
        ("[0,1]", 0, True),
        ("[0,1]", 0.5, True),
        ("[0,1]", 1, True),
        ("[0,1]", -0.1, False),
        ("[0,1]", 1.1, False),
        # Open intervals
        ("(0,1)", 0, False),
        ("(0,1)", 0.5, True),
        ("(0,1)", 1, False),
        # Mixed intervals
        ("[0,1)", 0, True),
        ("[0,1)", 1, False),
        ("(0,1]", 0, False),
        ("(0,1]", 1, True),
        # Infinite bounds
        ("(-inf, 0]", -1e10, True),
        ("(-inf, 0]", 0, True),
        ("(-inf, 0]", 1, False),
        ("[0, inf)", 0, True),
        ("[0, inf)", 1e10, True),
        ("[0, inf)", -1, False),
        # Float/int mix
        ("[0,2.5]", 2.5, True),
        ("[0,2.5]", 2, True),
        ("[0,2.5]", 0, True),
    ],
)
def test_real_value_within_interval(interval_str, value, should_pass):
    class Example:
        x = RealNumberWithinInterval(interval_str)

    e = Example()
    if should_pass:
        e.x = value
        assert e.x == value
    else:
        with pytest.raises(ValueError):
            e.x = value


# ----------------------------
# Test allow_none parameter
# ----------------------------


@pytest.mark.parametrize(
    "interval_str, value, should_pass",
    [
        ("[0,1]", None, False),  # None not allowed
        ("[0,1]", 0.5, True),
    ],
)
def test_real_value_within_interval_doesnt_allow_none(
    interval_str, value, should_pass
):
    class Example:
        x = RealNumberWithinInterval(interval_str)

    e = Example()
    if should_pass:
        e.x = value
        assert e.x == value
    else:
        with pytest.raises(TypeError):
            e.x = value


# ----------------------------
# Test invalid interval definitions
# ----------------------------


@pytest.mark.parametrize(
    "interval_str",
    [
        "[1,0]",  # lower > upper
        "(5,2)",  # lower > upper
        "[a,b]",  # non-numeric
        "0,1",  # missing brackets
        "(0,1",  # missing right bracket
        "[0,1)",  # valid, should not raise; included for contrast
    ],
)
def test_real_value_within_interval_invalid_definition(interval_str):
    if interval_str in ["[0,1)"]:
        # valid interval
        RealNumberWithinInterval(interval_str)  # should not raise
    else:
        with pytest.raises(Exception):
            RealNumberWithinInterval(interval_str)


# ----------------------------
# Test edge cases for boundaries
# ----------------------------


@pytest.mark.parametrize(
    "interval_str, boundary_value, expected",
    [
        ("[0,1]", 0, True),
        ("[0,1]", 1, True),
        ("(0,1)", 0, False),
        ("(0,1)", 1, False),
        ("[0,1)", 1, False),
        ("(0,1]", 0, False),
        ("(-inf, inf)", -1e100, True),
        ("(-inf, inf)", 1e100, True),
    ],
)
def test_real_value_within_interval_boundaries(
    interval_str, boundary_value, expected
):
    class Example:
        x = RealNumberWithinInterval(interval_str)

    e = Example()
    if expected:
        e.x = boundary_value
        assert e.x == boundary_value
    else:
        with pytest.raises(ValueError):
            e.x = boundary_value

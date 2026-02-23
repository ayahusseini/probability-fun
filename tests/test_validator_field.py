import pytest
import math
from numbers import Real
from probability_simulator.validation import RealNumber, Field


# ------------------------------
# Field Tests
# ------------------------------


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
        (str, "abs", True, False),
        (str, "abs", False, False),
        (str, None, False, True),
        (int, 3, False, False),  # 3 is a valid integer
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


# Test the delete functionality
def test_field_delete():
    class Example:
        x = Field(expected_type=int)

    e = Example()
    e.x = 10
    assert e.x == 10
    del e.x
    with pytest.raises(AttributeError):
        x_accessed = e.x


# Test the name functionality
def test_field_name_in_dict():
    class Example:
        x = Field(expected_type=int)

    e = Example()
    e.x = 10
    assert "x" in e.__dict__


# Test the get functionality with no instance
def test_field_get_with_no_instance():
    class Example:
        x = Field(expected_type=int)

    assert isinstance(Example.x, Field)


# ------------------------------
# RealNumber Tests
# ------------------------------


@pytest.fixture
def example_realnumber_autoconvert():
    class Example:
        y = RealNumber(auto_convert=True)

    return Example


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
        (3, 3.0),
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


# Test RealNumber preprocessing of inputs after assignment
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("inf", float("inf")),
        ("+inf", float("inf")),
        ("-inf", float("-inf")),
        ("infinity", float("inf")),
        ("-infinity", float("-inf")),
        ("3.14", 3.14),
        (3, 3.0),
        (3.0, 3.0),
        (0, 0),
    ],
)
def test_realnumber_preprocessing(input_str, expected):
    class Example:
        x = RealNumber()

    e = Example()
    e.x = input_str
    assert e.x == expected
    assert isinstance(e.x, Real)


# test real number with autoconvert off
@pytest.mark.parametrize(
    "input_str, expected, expectederr",
    [
        ("inf", float("inf"), True),
        ("+inf", float("inf"), True),
        ("-inf", float("-inf"), True),
        ("infinity", float("inf"), True),
        ("-infinity", float("-inf"), True),
        ("3.14", 3.14, True),
        (3, 3, False),
        (3.0, 3.0, False),
        (0, 0, False),
        (2.1, 2.1, False),
    ],
)
def test_realnumber_preprocessing_no_autoconvert(
    input_str, expected, expectederr
):
    class Example:
        x = RealNumber(auto_convert=False)

    e = Example()
    if expectederr:
        with pytest.raises(Exception):
            e.x = input_str
    else:
        e.x = input_str
        assert e.x == expected
        assert isinstance(e.x, Real)

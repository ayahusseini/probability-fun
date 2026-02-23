import re
from .fields import RealNumber, Field
from numbers import Real
from enum import Enum
from typing import Any


class IntervalBracket(Enum):
    left_open = "("
    left_closed = "["
    right_open = ")"
    right_closed = "]"

    @property
    def is_left(self) -> bool:
        return self in {self.left_open, self.left_closed}

    @property
    def is_right(self) -> bool:
        return self in {self.right_open, self.right_closed}

    @property
    def is_closed(self) -> bool:
        return self in {self.left_closed, self.right_closed}

    @property
    def is_open(self) -> bool:
        return self in {self.left_open, self.right_open}


class Interval:
    """
    Represents a mathematical interval defined by string notation.

    Examples:
        "(1,2)"
        "[0,1]"
        "(-inf, 5]"
        "[0, inf)"

    Notes
    - '(' and ')' denote open bounds.
    - '[' and ']' denote closed bounds.
    - Bounds may be finite numbers or ±inf.
    """

    lower = RealNumber(allow_none=False, auto_convert=True)
    upper = RealNumber(allow_none=False, auto_convert=True)

    @staticmethod
    def extract_pattern_components(interval_string: str) -> tuple[str]:
        """Return the left bracket, lower bound, upper bound, right bracket
        components
        from an interval string pattern (e.g. "[1,2]")
        """

        Field.validate_type(
            interval_string, str, "interval_string", allow_none=False
        )
        interval_string = interval_string.replace(" ", "")
        pattern = re.compile(
            r"^\s*([\(\[])\s*([^,]+)\s*,\s*([^,\]]+)\s*([\)\]])\s*$"
        )

        match = pattern.match(interval_string)

        if not match:
            raise ValueError(f"Invalid interval definition: {interval_string}")

        left_bracket, lower, upper, right_bracket = match.groups()
        return left_bracket, lower, upper, right_bracket

    def __init__(self, definition: str):

        left_br, left, right, right_br = self.extract_pattern_components(
            definition
        )
        self.left_bracket = IntervalBracket(left_br)
        self.right_bracket = IntervalBracket(right_br)
        self.lower = left
        self.upper = right

        if self.lower > self.upper:
            raise ValueError(
                f"Lower bound {self.lower} cannot exceed upper bound",
                f"{self.upper}",
            )

    def __contains__(self, value: Any) -> bool:
        # Validate input is a real number
        Field.validate_type(value, Real, "value", allow_none=False)

        # Lower bound check
        if self.left_bracket.is_closed:
            if value < self.lower:
                return False
        else:
            if value <= self.lower:
                return False

        # Upper bound check
        if self.right_bracket.is_closed:
            if value > self.upper:
                return False
        else:
            if value >= self.upper:
                return False

        return True

    def __repr__(self):
        return (
            f"{self.left_bracket.value}{self.lower}"
            + f", {self.upper}{self.right_bracket.value}"
        )

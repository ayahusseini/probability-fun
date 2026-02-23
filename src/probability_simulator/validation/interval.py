import math
import re
from .fields import RealNumber
from enum import Enum


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

    lower = RealNumber()
    upper = RealNumber()

    @staticmethod
    def extract_pattern_components(interval_string: str) -> tuple[str]:
        """Return the left bracket, lower bound, upper bound, right bracket
        components
        from an interval string pattern (e.g. "[1,2]")
        """
        pattern = re.compile(
            r"^\s*([\(\[])\s*([^,]+)\s*,\s*([^,\]]+)\s*([\)\]])\s*$"
        )

        match = pattern.match(interval_string)

        if not match:
            raise ValueError(f"Invalid interval definition: {interval_string}")

        left_bracket, lower, upper, right_bracket = match.groups()
        return left_bracket, lower, upper, right_bracket

    def __init__(self, definition: str):
        pattern_components = self.extract_pattern_components(definition)

        self.left_closed = pattern_components[0] == "["
        self.right_closed = pattern_components[-1] == "]"

        self.lower = self.parse_number(pattern_components[1])
        self.upper = self.parse_number(pattern_components[2])

        if (
            self.lower is not None
            and self.upper is not None
            and self.lower > self.upper
        ):
            raise ValueError("Lower bound must not exceed upper bound")

    @staticmethod
    def parse_number(number_txt: str):
        """Parse a string representing a number and return
        a
        """
        number_txt = number_txt.strip().lower()

        if number_txt in {"-inf", "-infinity"}:
            return -math.inf
        if number_txt in {"inf", "+inf", "infinity"}:
            return math.inf

        try:
            return float(number_txt)
        except ValueError:
            raise ValueError(f"Invalid numeric bound: {number_txt}")

    def __contains__(self, value) -> bool:
        if not isinstance(value):
            return False

        # Lower bound check
        if self.lower is not None:
            if self.left_closed:
                if value < self.lower:
                    return False
            else:
                if value <= self.lower:
                    return False

        # Upper bound check
        if self.upper is not None:
            if self.right_closed:
                if value > self.upper:
                    return False
            else:
                if value >= self.upper:
                    return False

        return True

    def __repr__(self):
        left = "[" if self.left_closed else "("
        right = "]" if self.right_closed else ")"
        return f"{left}{self.lower}, {self.upper}{right}"

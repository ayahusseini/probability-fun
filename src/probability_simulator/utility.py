"""Helper functions"""

import inspect


def is_callable(fn: callable) -> bool:
    """Returns True if fn is a callable"""
    return callable(fn)


def in_inclusive_range(count: int, mincount: int | None, maxcount: int | None) -> bool:
    """
    Returns True if count is within some inclusive range.
    If either mincount or maxcount are None, then they are treated as open
    intervals.
    """

    if mincount is None and maxcount is None:
        return True

    elif mincount is None:
        return count <= maxcount

    elif maxcount is None:
        return mincount <= count

    return mincount <= count <= maxcount


if __name__ == "__main__":

    def test(x: int, y) -> int:
        return None

    p = inspect.signature(test).parameters

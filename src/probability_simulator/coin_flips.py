"""Module for simulating coin flips"""

import numpy as np


class Coin:
    """Class representing a coin"""

    def __init__(self, bias=0.5, rng=None, initial_state=None):
        """Initialize the coin with a given bias

        bias: probability of landing on heads (1), default is 0.5 for a fair coin
        """
        self.bias = bias
        self.rng = np.random.default_rng() if rng is None else rng
        self.state = initial_state if initial_state else self.flip()

    @staticmethod
    def _validate_params(bias, initial_state):
        """Raise an error if a parameter is invalid"""
        if not (isinstance(bias, float) or (bias is None)):
            raise TypeError(
                f"Bias should be a float or None. Supplied {type(bias)}, {bias}"
            )
        if isinstance(bias, float) and (not 0 <= bias <= 1):
            raise ValueError(f"Bias should be in the range [0,1]. Supplied {bias}")
        if not (isinstance(initial_state, int) or (initial_state is None)):
            raise ValueError(
                f"initial_state should be an integer (0 or 1) or None. Supplied {type(initial_state)}, {initial_state}"
            )
        if isinstance(initial_state, int) and (not int in [0, 1]):
            raise ValueError(
                f"initial_state should be an integer (0 or 1). Supplied {initial_state}"
            )

    def flip(self):
        """Simulate flipping the coin"""
        self.state = 1 if self.rng.random() < self.bias else 0
        return self.state

    def flip_n(self, n: int):
        """Simulate flipping the coin n times"""
        return (self.rng.random(n) < self.bias).astype(int)

    def __str__(self) -> str:
        """String representation of the coin"""
        return "H" if self.state == 1 else "T"

    def __repr__(self) -> str:
        """Official string representation of the coin"""
        return f"Coin(bias={self.bias})"

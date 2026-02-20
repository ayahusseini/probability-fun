"""Module for simulating coin flips"""

import numpy as np

from numbers import Real


class Coin:
    """Class representing a coin"""

    def __init__(self, bias=0.5, rng=None, initial_state=None) -> None:
        """Initialize the coin with a given bias

        bias: probability of landing on heads (1), default is 0.5 for a fair coin
        """
        self.bias = bias
        self._validate_params(bias, initial_state)
        self.rng = np.random.default_rng() if rng is None else rng
        self.state = """Module for simulating coin flips"""


import numpy as np


class Coin:
    """Class representing a coin"""

    def __init__(self, bias=0.5, rng=None) -> None:
        """Initialize the coin with a given bias

        bias: probability of landing on heads (1), default is 0.5 for a fair coin
        rng: random number generator - samples from Uniform(0, 1)
        """
        self._validate_params(bias, rng)
        self.rng = np.random.default_rng() if rng is None else rng
        self.bias = bias

    @staticmethod
    def _validate_params(bias, rng) -> None:
        """Raise an error if a parameter is invalid"""

        if not ((rng is None) or (hasattr(rng, "random") and callable(rng.random))):
            raise TypeError(f"""rng should be a random number generator with a .random() attribute.
                            Supplied rng {(type(rng))} = {rng}""")

        if not (isinstance(bias, Real) or (bias is None)):
            raise TypeError(
                f"""Bias should be a Real number or None. 
                Supplied bias ({type(bias)}) = {bias}"""
            )

        elif isinstance(bias, float) and (not 0 <= bias <= 1):
            raise ValueError(f"""Bias should be in the range [0,1]. 
                             Supplied bias = {bias}""")

    def flip(self) -> int:
        """Simulate flipping the coin"""
        return int(self.rng.random() < self.bias)

    def flip_n(self, n: int) -> np.ndarray:
        """Simulate flipping the coin n times"""
        return (self.rng.random(n) < self.bias).astype(int)

    def __str__(self) -> str:
        """String representation of the coin"""
        return "H" if self.flip() == 1 else "T"

    def __repr__(self) -> str:
        """Official string representation of the coin"""
        return f"Coin(bias={self.bias})"

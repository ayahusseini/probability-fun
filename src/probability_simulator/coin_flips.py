"""coin_flips.py : Module for simulating coin flips"""

import numpy as np
import inspect

from numbers import Real


class Coin:
    """Class representing a coin"""

    def __init__(self, bias=0.5, rng=None) -> None:
        """Initialize the coin with a given bias.

        bias: probability of landing on heads (1), default is 0.5 for a fair
        coin
        rng: random number generator - samples from Uniform(0, 1)
        """
        self._validate_params(bias, rng)
        self.rng = np.random.default_rng() if rng is None else rng
        self.bias = bias

    @staticmethod
    def _validate_params(bias, rng) -> None:
        """Raise an error if a parameter is invalid"""

        if not (
            (rng is None) or (hasattr(rng, "random") and callable(rng.random))
        ):
            raise TypeError(f"""rng should be a random number generator with a 
                            .random() attribute.
                            Supplied rng {(type(rng))} = {rng}""")

        if not (isinstance(bias, Real) or (bias is None)):
            raise TypeError(
                f"""Bias should be a Real number or None. 
                Supplied bias ({type(bias)}) = {bias}"""
            )

        elif isinstance(bias, Real) and (not 0 <= bias <= 1):
            raise ValueError(f"""Bias should be in the range [0,1]. 
                             Supplied bias = {bias}""")

    def flip(self) -> int:
        """Simulate flipping the coin"""
        return int(self.rng.random() < self.bias)

    def flip_n(self, n: int) -> np.ndarray:
        """Simulate flipping the coin n times"""
        return (self.rng.random(n) < self.bias).astype(int)

    def __repr__(self) -> str:
        """Official string representation of the coin"""
        return f"Coin(bias={self.bias})"


class CoinExperiment:
    """Class for running experiments"""

    def __init__(self, coin: Coin, ntrials: int = 10000):
        self.ntrials = 10000
        self.coin = coin

    @classmethod
    def create_seeded_experiment(
        cls, coin: Coin, ntrials: int = 10000, seed: int = 43
    ):
        """Create a reproducable experiment"""
        seededrng = np.random.default_rng(seed=seed)
        coin.rng = seededrng
        return cls(coin, ntrials)

    def run_trials(self, trial_function: callable):
        """Run multiple trials"""
        # TODO validate the trial function

        return np.array(
            [trial_function(self.coin) for _ in range(self.ntrials)]
        )

    @staticmethod
    def flips_until(stopping_condition: callable):
        """Returns a function flips_until_stopping_condition
        which flips a coin until some stopping condition is met
        """
        # TODO decide if this should be some sort of a wrapper


if __name__ == "__main__":

    def r(x: int, y):
        return 3

    params = inspect.signature(r).parameters
    print(params)

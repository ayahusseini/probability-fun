"""coin_flips.py : Module for simulating coin flips using descriptors"""

import numpy as np
from typing import Callable, Any
from probability_simulator.validation import (
    RealNumberWithinInterval,
    Field,
    CallableField,
)


class Coin:
    """Class representing a coin"""

    bias = RealNumberWithinInterval(interval="[0,1]", auto_convert=True)

    def __init__(self, bias=0.5, rng=None) -> None:
        """Initialize the coin with a given bias.

        bias: probability of landing on heads (1),
            default is 0.5 for a fair coin
        rng: random number generator - samples from Uniform(0, 1)
        """
        self.rng = np.random.default_rng() if rng is None else rng
        self.bias = bias  # RealNumber descriptor will validate automatically
        self._validate_rng(self.rng)

    @staticmethod
    def _validate_rng(rng) -> None:
        """Validate that rng has a callable .random() method"""
        if not (hasattr(rng, "random") and callable(rng.random)):
            raise TypeError(
                "rng should be a random number generator",
                f"with a callable .random() method.Got {type(rng)} = {rng}",
            )

    def flip(self) -> int:
        """Simulate flipping the coin once"""
        return int(self.rng.random() < self.bias)

    def flip_n(self, n: int) -> np.ndarray:
        """Simulate flipping the coin n times"""
        Field.validate_type(n, int, "n (number of trials)", allow_none=False)
        if n < 1:
            raise ValueError(f"n must be a positive integer, got {n}")
        return (self.rng.random(n) < self.bias).astype(int)

    def __repr__(self) -> str:
        return f"Coin(bias={self.bias})"


class CoinExperiment:
    """Class for running coin flip experiments"""

    ntrials = Field(expected_type=int)
    trial_function = CallableField()

    def __init__(self, coin: Coin, ntrials: int = 10000):
        self.coin = coin
        self.ntrials = ntrials

    @classmethod
    def create_seeded_experiment(
        cls, coin: Coin, ntrials: int = 10000, seed: int = 43
    ):
        """Create a reproducible experiment with a seeded RNG"""
        seeded_rng = np.random.default_rng(seed=seed)
        coin.rng = seeded_rng
        return cls(coin, ntrials)

    def run_trials(self, trial_function: Callable[[Coin], Any]) -> np.ndarray:
        """Run multiple trials using a provided trial function"""
        # Validate the trial function using CallableField logic
        CallableField._validate_callable(trial_function, "trial_function")
        self.trial_function = trial_function
        return np.array(
            [trial_function(self.coin) for _ in range(self.ntrials)]
        )

    @staticmethod
    def flips_until(
        stopping_condition: Callable[[int], bool],
    ) -> Callable[[Coin], int]:
        """
        Returns a function that flips a coin until
        `stopping_condition` is met.
        """
        CallableField._validate_callable(
            stopping_condition, "stopping_condition"
        )

        def flip_func(coin: Coin) -> int:
            count = 0
            while True:
                count += 1
                if stopping_condition(coin.flip()):
                    break
            return count

        return flip_func

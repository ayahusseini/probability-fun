"""Module for simulating coin flips"""
import numpy as np 

class Coin:
    """Class representing a coin"""

    def __init__(self, bias=0.5, rng= None):
        """Initialize the coin with a given bias
        
        bias: probability of landing on heads (1), default is 0.5 for a fair coin
        """
        self.bias = bias
        self.state = 1
        self.rng = np.random.default_rng() if rng is None else rng

    def flip(self):
        """Simulate flipping the coin"""
        self.state = 1 if self.rng.random() < self.bias else 0
        return self.state
    
    def flip_n(self, n: int):
        """Simulate flipping the coin n times"""
        return (self.rng.random(n) < self.bias).astype(int)

    def __str__(self) -> str:
        """String representation of the coin"""
        return f"Coin(bias={self.bias})"

    def __repr__(self) -> str:
        """Official string representation of the coin"""
        return "H" if self.state == 1 else "T"
        
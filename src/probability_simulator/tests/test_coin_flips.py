import numpy as np
from pytest import fixture
from probability_simulator.coin_flips import Coin

@fixture
def fair_coin():
    """Fixture for creating a coin instance"""
    return Coin(bias = 0.5)

def test_coin_flip(fair_coin):
    """Test that a fair coin flip returns either 0 or 1"""
    assert fair_coin.flip() in [0, 1]
    
def test_coin_flip_n_is_array(fair_coin):
    """Test that many fair coin flips return an array"""
    assert isinstance(fair_coin.flip_n(n = 12),np.ndarray) 
    
def test_coin_flip_n_is_array(fair_coin):
    """Test that many fair coin flips return an array"""
    assert isinstance(fair_coin.flip_n(n = 12),np.ndarray) 
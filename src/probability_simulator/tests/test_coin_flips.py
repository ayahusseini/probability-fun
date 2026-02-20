import numpy as np
import pytest
from probability_simulator.coin_flips import Coin


@pytest.fixture
def fair_coin():
    """Fixture for creating a coin instance"""
    return Coin(bias=0.5)


def test_text_representation(fair_coin):
    assert f"{fair_coin}" in ["H", "T"]


def test_coin_flip(fair_coin):
    """Test that a fair coin flip returns either 0 or 1"""
    assert fair_coin.flip() in [0, 1]


def test_coin_flip_n_is_array(fair_coin):
    """Test that many fair coin flips return an array"""
    assert isinstance(fair_coin.flip_n(n=12), np.ndarray)


def test_coin_flip_n_is_array_of_1s_and_0s(fair_coin):
    """Test that many fair coin flips return an array of 1s and 0s"""
    result = fair_coin.flip_n(n=12)
    assert all(x in [0, 1] for x in result)


def test_two_different_rngs_give_different_results():
    """Test that two different RNGs give different results"""
    coin1 = Coin(bias=0.5)
    coin2 = Coin(bias=0.5)
    result1 = coin1.flip_n(n=100)
    result2 = coin2.flip_n(n=100)
    assert not np.array_equal(result1, result2)


def test_same_rngs_give_same_results():
    """Test that two different RNGs give different results"""
    r1 = np.random.default_rng(seed=42)
    r2 = np.random.default_rng(seed=42)
    coin1 = Coin(bias=0.5, rng=r1)
    coin2 = Coin(bias=0.5, rng=r2)
    result1 = coin1.flip_n(n=1000)
    result2 = coin2.flip_n(n=1000)
    assert np.array_equal(result1, result2)


def test_invalid_bias_type():
    with pytest.raises(TypeError):
        Coin(bias="1.0")


def test_integer_is_valid_bias_type():
    Coin(bias=1)

import pytest

def calc_price(base_price: float, discount: float, count: int) -> float:
    pass

def test_calc_price():
    with pytest.raises(ValueError):
        calc_price(base_price=0.0, discount=0.1, count=2)


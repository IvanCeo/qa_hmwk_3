import pytest

class Event():
    def __init__(self, id, base_price: float, avaliable_tickets: int, booked_tickets: int):
        self.id = id
        self.base_price = base_price
        self.avaliable_tickets = avaliable_tickets
        self.booked_tickets = booked_tickets


def calc_price(base_price: float, discount: float, count: int) -> float:
    if (
        count == 0 or
        discount < 0 or
        discount > base_price or
        base_price < 0 or
        isinstance(count, int) or
        isinstance(base_price, float) or
        isinstance(discount, float)
    ):
        raise ValueError
    else:
        return (base_price - discount)* count


@pytest.mark.parametrize(
        "base_price, discount, count",
        [
            (0.0, 0.1, 2),
            (12, 1, -3),
        ]
)
def test_calc_price(base_price, discount, count):
    with pytest.raises(ValueError):
        calc_price(base_price, discount, count)
    



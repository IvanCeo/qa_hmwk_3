import pytest

class Event():
    def __init__(self, available_tickets: int, id = 1):
        self.id = id
        self.available_tickets = available_tickets
    
    def check_availability(self, seats_requested: int) -> bool:
        if not isinstance(seats_requested, int):
            raise TypeError
        match seats_requested:
            case _ if seats_requested <= 0:
                raise ValueError
            case _:
                if self.available_tickets >= seats_requested:
                    return True
                return False
            
class TestEvent():
    """
    mark = 1 - Negative case
    mark = 3 - Positive case
    """
    @pytest.mark.parametrize(
        "mark, available_tickets, seats_requested, expected",
        [
            (1, 1, 1.3, TypeError),
            (1, 1, "2", TypeError),
            (1, 1, -3, ValueError),
            (1, 1, 0, ValueError),
            (2, 4, 2, True),
            (2, 4, 5, False),
        ]
    )
    def test_check_availability(self, mark, available_tickets, seats_requested, expected):
        event = Event(available_tickets)
        match mark:
            case 1:
                with pytest.raises(expected):
                    event.check_availability(seats_requested)
            case 2:
                event.check_availability(seats_requested) == expected



def calc_price(base_price: float, discount: float, count: int) -> float:
    if (
        count <= 0 or
        discount < 0 or
        discount > base_price or
        base_price < 0
    ):
        raise ValueError
    elif (
        not isinstance(count, int) or
        not isinstance(base_price, (float, int)) or
        not isinstance(discount, (float, int))
    ):
        raise TypeError
    else:
        return (base_price - discount)* count


@pytest.mark.parametrize(
        "base_price, discount, count, expected",
        [
            (0.0, 0.1, 2, ValueError),
            (12, 1, -3, ValueError),
            (10, -1, 5, ValueError),
            (10, 11, 5, ValueError),
            (10.5, 2.5, 0, ValueError),
            ("10", 2, 3, TypeError),
            (10, "2", 3, TypeError),
            (10.5, 2.5, 3.5, TypeError),
            (10.0, 2.0, 3, 24.0),
            (15, 5, 4, 40.0),
            (10.5, 0.5, 2, 20.0),
            (100, 0, 10, 1000.0),
        ]
)
def test_calc_price(base_price, discount, count, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            calc_price(base_price, discount, count)
    elif expected is TypeError:
        with pytest.raises(TypeError):
            calc_price(base_price, discount, count)
    else:
        assert calc_price(base_price, discount, count) == expected
    

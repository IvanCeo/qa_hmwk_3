import pytest
from datetime import date, timedelta, datetime
from random import randint, choice, randrange
import uuid
import hashlib

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
    
class PromoCode():
    def __init__(self, date: date, counter: int, valid: bool):
        self.is_valid = valid
        self.works_until = datetime.strptime(date, '%Y-%m-%d').date()
        self.availability_counter = counter
    
    def apply_promocode(self) -> bool:
        if (
            self.is_valid == False or
            self.works_until < date.today() or
            self.availability_counter <= 0
        ):
            return False
        self.availability_counter -= 1
        if self.availability_counter <= 0:
            self.is_valid = False
        return True
    
class TestPromocode():
    def get_rand_date(start_year=2024, end_year=2026):
        delta_days = (date(end_year, 12, 31) - date(start_year, 1, 1)).days
        random_days = randrange(delta_days + 1)
        return date(start_year, 1, 1) + timedelta(random_days)
    
    # def __init__(self):
    #     self.promocodeStorage = {}

    #     for _ in range(20):
    #         self.promocodeStorage[str(uuid.uuid1())] = PromoCode(
    #             date=self.get_rand_date(), 
    #             counter=randint(0, 10), 
    #             valid=choice([True, False])
    #         )

    #     self.promocodeStorage['ee21cb76-3005-11f0-a671-803253436fb5'] = PromoCode(
    #         date=self.get_rand_date(), 
    #         counter=randint(0, 10), 
    #         valid=choice([True, False])
    #     )

    @pytest.mark.parametrize(
            "date, counter, valid, expected",
            [
                ('2025-10-12', 3, True, True),
                ('2025-10-12', 3, False, False),
                ('2025-10-12', 0, True, False),
                ('2025-01-12', 3, True, False),
            ]
    )
    def test_apply_promocode(self, date, counter, valid, expected):
        promo = PromoCode(date, counter, valid)
        assert promo.apply_promocode() == expected

def generate_booking_ref(user_id: int, event_id: int):
    if (
        not isinstance(user_id, int) or
        not isinstance(event_id, int)
    ):
        raise TypeError
    else:
        data = str(user_id) + str(event_id)
        hash_object = hashlib.md5(data.encode())
        md5_hash = hash_object.hexdigest()
        return md5_hash + str(uuid.uuid1())

@pytest.mark.parametrize(
    "mark, user_id, event_id, expected",
    [
        (1, '12', 13, TypeError),
        (2, 12, 13, True),
    ]    
)    
def test_generate_booking_ref(mark, user_id, event_id, expected):
    match mark:
        case 1:
            with pytest.raises(expected):
                generate_booking_ref(user_id, event_id)
        case 2:
            ref1 = generate_booking_ref(user_id, event_id)
            ref2 = generate_booking_ref(user_id, event_id)
            assert (ref1 != ref2) == expected

def mock_email(email: str) -> bool:
    if not isinstance(email, str):
        raise TypeError
    return choice[True, False]
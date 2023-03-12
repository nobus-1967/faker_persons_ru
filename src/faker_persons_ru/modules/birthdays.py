"""Module for generating birthdays of fake Russian persons."""
import datetime
import random

from faker_persons_ru.modules.demography import Age


def gen_birthdays(age: Age, amount: int) -> list[str]:
    """Generate random birthdays for a certain age.

    Args:
        age: An object of dataclass 'Age' for a certain age.
        amount: An amount (int) of male/female persons of a certain age.

    Returns:
        A list (of str) containing dates of birth from datetime (YYYY-MM-DD) for
        fake Russian people of a certain age.
    """
    date_start = datetime.datetime(age.year_start, 1, 1)
    date_end = datetime.datetime(age.year_end, 12, 31)
    date_delta = datetime.timedelta(days=1)

    dates_lst: list[str] = []
    birthdays_lst: list[str] = []
    date = date_start

    while date <= date_end:
        dates_lst.append(date.strftime('%Y-%m-%d'))
        date += date_delta

    birthdays_lst = random.choices(dates_lst, k=amount)

    return birthdays_lst

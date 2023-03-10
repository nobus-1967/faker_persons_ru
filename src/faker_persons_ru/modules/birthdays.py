"""Module for generating birthdays of fake Russian persons."""
import datetime
import random

from faker_persons_ru.modules.demography import Age


def gen_birthdays(age: Age, amount: int) -> list[str]:
    """Generate random birthdays for a certain age.

    Args:
        age: object - An object of dataclass 'Age' (certain age).
        amount: int - An amount of male/female persons of a certain age.

    Returns:
        A list (str) containing dates of birth from datetime (YYYY-MM-DD) for
        fake Russian people of a certain age.
    """
    start_date = datetime.datetime(age.start_year, 1, 1)
    end_date = datetime.datetime(age.end_year, 12, 31)
    time_delta = datetime.timedelta(days=1)

    dates_lst: list[str] = []
    birthdays_lst: list[str] = []

    while start_date <= end_date:
        dates_lst.append(start_date.strftime('%Y-%m-%d'))
        start_date += time_delta

    birthdays_lst = random.choices(dates_lst, k=amount)

    return birthdays_lst

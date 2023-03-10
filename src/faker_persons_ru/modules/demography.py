"""Module for generating age/sex values for fake Russian datasets."""
import datetime
import random

from collections import namedtuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Age:
    """A dataclass for different ages."""

    group: str
    proportion: float
    start_year: int
    end_year: int
    female: float

    def gen_birthday(self) -> str:
        """Generate a random birthday for the age.

        Returns:
            A str from datetime containing date of birth (YYYY-MM-DD).
        """
        start_date = datetime.datetime(self.start_year, 1, 1)
        end_date = datetime.datetime(self.end_year, 12, 31)
        random_timest = random.randint(
            int(start_date.timestamp()), int(end_date.timestamp())
        )
        birthday = datetime.datetime.fromtimestamp(random_timest)

        return birthday.strftime('%Y-%m-%d')


Sex = namedtuple('Sex', ['male', 'female'])


def calc_ages(total: int) -> tuple[int, int, int]:
    """Calculate amounts of fake persons of each age.

    Args:
        total: int - A total amount of fake personal records; from user input.

    Returns:
        A tuple (of int) representing amounts of fake persons of a certain age.
    """
    total_j, total_m, total_s = 0, 0, 0

    if total < 10:
        while total > 0:
            total_j += 1
            total -= 1
            if total > 2:
                total_s += 1
                total_j += 1
                total -= 2
            elif total == 2:
                total_s += 1
                total -= 1
    elif total >= 10:
        total_j += int(total * JUNIOR.proportion)
        total_s += int(total * SENIOR.proportion)
        total_m += total - (total_j + total_s)

    return total_j, total_m, total_s


def calc_sex(total_age: int, female_age: float) -> tuple[int, int]:
    """Calculate amounts of fake persons of each sex.

    Args:
        total_age: int - A total amount of fake personal records; from user input.
        female_age: float - A females' percent in the ages.

    Returns:
        A tuple (of int) representing amounts of male/female persons.
    """
    male, female = 0, 0

    if total_age == 1:
        male = 1 if female_age < 0.5 else 0
        female = 1 if female_age > 0.5 else 0
    elif total_age == 2:
        male = 1
        female = 1
    elif total_age > 2:
        female = int(total_age * female_age)
        male = total_age - female

    return male, female


JUNIOR = Age('J', 0.27, 1990, 2004, 0.49)
MIDDLE = Age('M', 0.42, 1973, 1989, 0.51)
SENIOR = Age('S', 0.31, 1958, 1972, 0.55)


SEX = Sex('муж.', 'жен.')

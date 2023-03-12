"""Module for generating age/sex values for fake Russian datasets."""
import random

from dataclasses import dataclass

SEX = ['муж.', 'жен.']


@dataclass(frozen=True)
class Age:
    """A dataclass for different ages."""

    group: str
    proportion: float
    year_start: int
    year_end: int
    females: float


def calc_age_amounts(total: int) -> tuple[int, int, int]:
    """Calculate amounts of persons of each age.

    Args:
        total: A total amount (int) of generatin fake records; from user input.

    Returns:
        A tuple (of int) representing amounts of persons of a certain age.
    """
    total_j, total_m, total_s = 0, 0, 0

    if total < 4:
        if total == 1:
            total_m += 1
        elif total == 2:
            total_m += 1
            total_s += 1
        elif total == 3:
            total_j += 1
            total_m += 1
            total_s += 1
    elif total >= 4:
        total_j += int(total * JUNIOR.proportion)
        total_s += int(total * SENIOR.proportion)
        total_m += total - (total_j + total_s)

    return total_j, total_m, total_s


def calc_sex_amounts(age_amount: int, females_pcent: float) -> tuple[int, int]:
    """Calculate total persons of each sex.

    Args:
        age_amount: An amount (int) of persons of a certain age.
        females_pcent: A percent (float) of female persons in the ages.

    Returns:
        A tuple (of int) representing amounts of male/female persons.
    """
    males, females = 0, 0

    if age_amount == 1:
        males += 1 if females_pcent < 0.5 else 0
        females += 1 if females_pcent > 0.5 else 0
    elif age_amount == 2:
        males += 1
        females += 1
    elif age_amount > 2:
        females += int(age_amount * females_pcent)
        males += age_amount - females

    return males, females


JUNIOR = Age('J', 0.27, 1990, 2004, 0.49)
MIDDLE = Age('M', 0.42, 1973, 1989, 0.51)
SENIOR = Age('S', 0.31, 1958, 1972, 0.55)

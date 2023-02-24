"""Module for create Russian names lists based on their weights."""
import random


def read_names(total: int, names_dict: dict[str, int]) -> list[str]:
    """Create lists of Russian first names, last names and patronymics .

    Args:
        total: integer - total amount of persons from user input.
        names_dict: dict - Russian names and their weights.

    Returns:
        list of names based on weights (frequency of use) for a certain amount
        of fake persons.
    """
    names = list(names_dict.keys())
    weights = list(names_dict.values())

    names_list = random.choices(names, weights=weights, k=total)

    return names_list

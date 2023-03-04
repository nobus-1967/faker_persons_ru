"""Module for create data lists based on their weights."""
import random


def read_names(total: int, names_dict: dict[str, int]) -> list[str]:
    """Create lists of Russian first names, last names and patronymics.

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


def read_locations(
    total: int, localities_dict: dict[str, tuple[str, int]]
) -> list[tuple[str, str]]:
    """Create lists of Russian localities (with regions) and their weights.

    Args:
        total: integer - total amount of persons from user input.
        localities_dict: dict - Russian localities (with regions) and their
        weights.

    Returns:
        list (tuple of strings) of localities and regions based on weights
        (according to population) for a certain amount of fake persons.
    """
    localities = list(localities_dict.keys())
    regions = [value[0] for value in localities_dict.values()]
    locations = list(zip(regions, localities))
    weights = [value[1] for value in localities_dict.values()]

    localities_list = random.choices(locations, weights=weights, k=total)

    return localities_list

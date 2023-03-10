"""Module for create data lists based on their weights."""
import random


def read_names(total: int, names_dict: dict[str, float]) -> list[str]:
    """Create lists of Russian first names, last names and patronymics.

    Args:
        total: int - A total amount of fake personal records; from user input.
        names_dict: dict - Russian names (keys, str) and corresponding weights
        (values, float).

    Returns:
        A list (of str) containing names based on weights (i.e.frequency of use)
        for a certain amount of fake Russian persons.
    """
    names = list(names_dict.keys())
    weights = list(names_dict.values())

    names_list = random.choices(names, weights=weights, k=total)

    return names_list


def read_locations(
    total: int, localities_dict: dict[str, tuple[str, float]]
) -> list[tuple[str, str]]:
    """Create lists of Russian localities (with regions) and their weights.

    Args:
        total: int - A total amount of fake personal records; from user input.
        localities_dict: dict - Russian localities (keys, str) with regions and
        their weights (values, tuple of str and float).

    Returns:
        A list (tuples of str) of localities and regions based on weights
        (according to population) for a certain amount of fake Russian persons.
    """
    localities = list(localities_dict.keys())
    regions = [value[0] for value in localities_dict.values()]
    locations = list(zip(regions, localities))
    weights = [value[1] for value in localities_dict.values()]

    localities_list = random.choices(locations, weights=weights, k=total)

    return localities_list

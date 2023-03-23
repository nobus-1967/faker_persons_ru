"""Module for create data lists based on their weights."""
import random


def read_name(total: int, names_dict: dict[str, float]) -> list[str]:
    """Create lists of Russian first names, last names and patronymics.

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        names_dict: Russian names (key, str) and their weights (value, float)
        as dict.

    Returns:
        A list (of str) representing names; based on weights (i.e. frequency of
        use) for a certain amount of persons.
    """
    names_from_dict = list(names_dict.keys())
    weights_from_dict = list(names_dict.values())

    name_lst = random.choices(
        names_from_dict, weights=weights_from_dict, k=total
    )

    return name_lst


def read_location(
    total: int, localities_dict: dict[str, tuple[str, float]]
) -> list[tuple[str, str]]:
    """Create lists of Russian piopulated localities with regions.

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        localities_dict: Russian locations (dict) mapping populated localities
        (keys, str) and their regions and weights (values, tuple of str).

    Returns:
        A list (tuple of strings) representing localities and regions; based
        on weights (according to population) for a certain amount of persons.
    """
    localities_from_dict = list(localities_dict.keys())
    regions_from_dict = [value[0] for value in localities_dict.values()]
    weights_from_dict = [value[1] for value in localities_dict.values()]
    locations_lst = list(zip(regions_from_dict, localities_from_dict))

    locality_lst = random.choices(
        locations_lst, weights=weights_from_dict, k=total
    )

    return locality_lst

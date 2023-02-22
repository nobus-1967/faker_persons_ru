"""Module for create names lists based on their weights."""
import random
import csv


def read_names(total: int, filename: str) -> list[str]:
    """Create lists of first names, lastnames and patronymics
    based on their weights (frequency of use).

    Args:
        total: integer of total persons from user input.
        filename: string with name of file contains names and their weights.

    Returns:
        list of names for a certain amount of fake persons.
    """
    names = list()
    weights = list()

    with open(filename, newline='') as csvfile:
        data_reader = csv.reader(
            csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC
        )

        for i, data in enumerate(data_reader):
            names.append(data[0])
            weights.append(data[1])

    names_lst = random.choices(names, weights=weights, k=total)

    return names_lst

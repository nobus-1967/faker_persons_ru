"""Module for generating fake Russian cell phone numbers."""
import random

CODES: list[str] = [
    '907',
    '935',
    '943',
    '944',
    '945',
    '946',
    '947',
    '948',
    '972',
    '973',
    '974',
    '975',
    '976',
]


def gen_phones(total: int) -> list[str]:
    """Generate a dataset of fake Russian cell phone numbers.

    Args:
        total: int - A total amount of fake personal records; from user input.

    Returns:
        A list (of str) containing fake Russian cell phone numbers.
    """
    phones_lst: list[str] = []
    phones_nums_dset = [num for num in range(1110011, 9990100)]
    random.shuffle(phones_nums_dset)

    for i in range(total):
        num = str(phones_nums_dset.pop())
        code = random.choice(CODES)
        phone = f'+7({code}){str(num)[:3]}-{str(num)[3:5]}-{str(num)[5:]}'

        phones_lst.append(phone)

    return phones_lst

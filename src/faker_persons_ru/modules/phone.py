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


def gen_phone(total: int) -> list[str]:
    """Generate a dataset of fake Russian cell phone numbers.

    Args:
        total: A total amount (int) of records/fake persons; from user input.

    Returns:
        A list of str representing fake Russian cell phone numbers.
    """
    phone_lst: list[str] = []
    phone_num_dset = [num for num in range(1110011, 9990100)]
    random.shuffle(phone_num_dset)

    for _ in range(total):
        num = str(phone_num_dset.pop())
        code = random.choice(CODES)
        phone = f'+7({code}){str(num)[:3]}-{str(num)[3:5]}-{str(num)[5:]}'

        phone_lst.append(phone)

    return phone_lst

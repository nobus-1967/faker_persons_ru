"""Module for generating fake Russian cell phone numbers."""
import random

CODES = [907, 935, 943, 944, 945, 946, 947, 948, 972, 973, 974, 975, 976]


def generate_phones(total: int) -> list[str]:
    """Generate a dataset of fake phones.

    Args:
        total: integer of total persons from user input.

    Returns:
        list of fake Russian cell phone numbers.
    """
    phones = [None] * total
    phones_nums = [num for num in range(1110011, 9990100)]
    random.shuffle(phones_nums)

    for i in range(total):
        num = str(phones_nums.pop())
        code = str(random.choice(CODES))
        phone = f'+7({code}){str(num)[:3]}-{str(num)[3:5]}-{str(num)[5:]}'

        phones[i] = phone

    return phones

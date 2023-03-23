"""
Module for generating datasets (fake Russian persons, contacts and locations).
"""
import random

from collections import deque
from itertools import product

from faker_persons_ru.modules import demography
from faker_persons_ru.modules.demography import Age, SEX
from faker_persons_ru.modules.demography import JUNIOR, MIDDLE, SENIOR
from faker_persons_ru.modules import birthday
from faker_persons_ru.modules import email
from faker_persons_ru.modules import phone
from faker_persons_ru.data import reader
from faker_persons_ru.data.last_names_male import LAST_NAMES_MALE
from faker_persons_ru.data.last_names_female import LAST_NAMES_FEMALE
from faker_persons_ru.data.first_names_j import FIRST_NAMES_MALE_J
from faker_persons_ru.data.first_names_j import FIRST_NAMES_FEMALE_J
from faker_persons_ru.data.first_names_m import FIRST_NAMES_MALE_M
from faker_persons_ru.data.first_names_m import FIRST_NAMES_FEMALE_M
from faker_persons_ru.data.first_names_s import FIRST_NAMES_MALE_S
from faker_persons_ru.data.first_names_s import FIRST_NAMES_FEMALE_S
from faker_persons_ru.data.patronymics_j import PATRONYMICS_MALE_J
from faker_persons_ru.data.patronymics_j import PATRONYMICS_FEMALE_J
from faker_persons_ru.data.patronymics_m import PATRONYMICS_MALE_M
from faker_persons_ru.data.patronymics_m import PATRONYMICS_FEMALE_M
from faker_persons_ru.data.patronymics_s import PATRONYMICS_MALE_S
from faker_persons_ru.data.patronymics_s import PATRONYMICS_FEMALE_S


def gen_base(total: int) -> list[list[str]]:
    """Generate a dataset of fake Russian data (name, sex, date of birth).

    Args:
        total: A total amount (int) of records/fake persons; from user input.

    Returns:
        A list (lists of str) containing fake Russian personal data.
    """
    # 1. Calculate age and sex values.
    ages = [JUNIOR, MIDDLE, SENIOR]

    demography_lst = product(ages, SEX)

    amounts = demography.calc_age_amount(total)

    amount_lst: list[int] = []

    for group in [
        (amount, ages.female_pcent) for amount, ages in zip(amounts, ages)
    ]:
        amount, female_pcent = group
        amount_lst += demography.calc_sex_amount(amount, female_pcent)

    # 2. Generate dataset.
    base_dset: list[list[str]] = []

    for i, part in enumerate(demography_lst):
        age, sex = part
        amount = amount_lst[i]

        last_names = LAST_NAMES_MALE if (sex == 'муж.') else LAST_NAMES_FEMALE
        if age.group == 'J':
            first_names = (
                FIRST_NAMES_MALE_J if (sex == 'муж.') else FIRST_NAMES_FEMALE_J
            )
            patronymics = (
                PATRONYMICS_MALE_J if (sex == 'муж.') else PATRONYMICS_FEMALE_J
            )
        if age.group == 'M':
            first_names = (
                FIRST_NAMES_MALE_M if (sex == 'муж.') else FIRST_NAMES_FEMALE_M
            )
            patronymics = (
                PATRONYMICS_MALE_M if (sex == 'муж.') else PATRONYMICS_FEMALE_M
            )
        if age.group == 'S':
            first_names = (
                FIRST_NAMES_MALE_S if (sex == 'муж.') else FIRST_NAMES_FEMALE_S
            )
            patronymics = (
                PATRONYMICS_MALE_S if (sex == 'муж.') else PATRONYMICS_FEMALE_S
            )

        dset = gen_person(
            age, sex, amount, last_names, first_names, patronymics
        )

        base_dset.extend(dset)

    random.shuffle(base_dset)

    return base_dset


def gen_person(
    age: Age,
    sex: str,
    amount: int,
    last_names: dict[str, float],
    first_names: dict[str, float],
    patronymics: dict[str, float],
) -> list[list[str]]:
    """Generate fake Russian data (name, sex, date of birth).

    Args:
        age: An object of dataclass 'Age' for a certain age.
        sex: A value(str) from namedtuple 'Sex'.
        amount: An amount (int) of male/female persons of a certain age.
        last_names: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).
        first_names: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).
        patronymics: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).

    Returns:
        A list (of lists of str) containing fake Russan personal data (name,
        sex, date of birth) of a certain sex and age.
    """
    person_lst: list[list[str]] = []
    birthday_dq = deque(birthday.gen_birthday(age, amount))

    last_names_dq = deque(reader.read_name(amount, last_names))
    first_names_dq = deque(reader.read_name(amount, first_names))
    patronymics_dq = deque(reader.read_name(amount, patronymics))

    for i in range(amount):
        date_of_birth = birthday_dq.popleft()

        person = [
            last_names_dq.popleft(),
            first_names_dq.popleft(),
            patronymics_dq.popleft(),
            sex,
            date_of_birth,
        ]

        if birthday_dq.count(date_of_birth) > 0:
            while person_lst.count(person) > 0:
                birthday_dq.append(person.pop())
                date_of_birth_new = birthday_dq.popleft()
                person.append(date_of_birth_new)

        person_lst.append(person)

    return person_lst


def gen_contact(total: int, base_dset: list[list[str]]) -> zip:
    """Generate a dataset of fake Russian contacts (cell phone numbers, emails).

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        base_dset: A dataset (list of lists of str) containing fake Russian
        personal data, including names and date of birth.

    Returns:
        A zipped tupple aggregating lists (of str) with fake Russian phones
        and emails.
    """
    phone_lst = phone.gen_phone(total)
    email_lst = email.gen_email(base_dset)

    contact_dset = zip(phone_lst, email_lst)

    return contact_dset


def gen_location(
    total: int, localities_dict: dict[str, tuple[str, float]]
) -> zip:
    """Generate dataset of Russian locations (region and populated locality.

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        localities_dict: Russian locations (dict) mapping populated localities
        (keys, str) and their regions and weights (values, tuple of str).

    Returns:
        A zipped tuple aggregating lists (of str) with Russian regions and
        populated localities.
    """
    region_lst: list[str] = []
    locality_lst: list[str] = []

    location_lst = reader.read_location(total, localities_dict)

    for location in location_lst:
        region_lst.append(location[0])
        locality_lst.append(location[1])

    location_dset = zip(region_lst, locality_lst)

    return location_dset

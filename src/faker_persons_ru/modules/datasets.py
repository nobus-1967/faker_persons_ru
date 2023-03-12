"""
Module for generating datasets (fake Russian persons, contacts and locations).
"""
import random

from collections import deque
from itertools import product

from faker_persons_ru.modules import demography
from faker_persons_ru.modules.demography import Age, SEX
from faker_persons_ru.modules.demography import JUNIOR, MIDDLE, SENIOR
from faker_persons_ru.modules import birthdays
from faker_persons_ru.modules import emails
from faker_persons_ru.modules import phones
from faker_persons_ru.data import reader
from faker_persons_ru.data.lastnames_male import LASTNAMES_MALE
from faker_persons_ru.data.lastnames_female import LASTNAMES_FEMALE
from faker_persons_ru.data.firstnames_j import FIRSTNAMES_MALE_J
from faker_persons_ru.data.firstnames_j import FIRSTNAMES_FEMALE_J
from faker_persons_ru.data.firstnames_m import FIRSNAMES_MALE_M
from faker_persons_ru.data.firstnames_m import FIRSNAMES_FEMALE_M
from faker_persons_ru.data.firstnames_s import FIRSNAMES_MALE_S
from faker_persons_ru.data.firstnames_s import FIRSNAMES_FEMALE_S
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

    amounts_total = demography.calc_age_amounts(total)

    amounts_lst: list[int] = []

    for group in [
        (amount_total, ages.females)
        for amount_total, ages in zip(amounts_total, ages)
    ]:
        amount_total, females_pcent = group
        amounts_lst += demography.calc_sex_amounts(amount_total, females_pcent)

    # 2. Generate dataset.
    base_dset: list[list[str]] = []

    for i, part in enumerate(demography_lst):
        age, sex = part
        amount = amounts_lst[i]

        lastnames = LASTNAMES_MALE if (sex == 'муж.') else LASTNAMES_FEMALE
        if age.group == 'J':
            firstnames = (
                FIRSTNAMES_MALE_J if (sex == 'муж.') else FIRSTNAMES_FEMALE_J
            )
            patronymics = (
                PATRONYMICS_MALE_J if (sex == 'муж.') else PATRONYMICS_FEMALE_J
            )
        if age.group == 'M':
            firstnames = (
                FIRSNAMES_MALE_M if (sex == 'муж.') else FIRSNAMES_FEMALE_M
            )
            patronymics = (
                PATRONYMICS_MALE_M if (sex == 'муж.') else PATRONYMICS_FEMALE_M
            )
        if age.group == 'S':
            firstnames = (
                FIRSNAMES_MALE_S if (sex == 'муж.') else FIRSNAMES_FEMALE_S
            )
            patronymics = (
                PATRONYMICS_MALE_S if (sex == 'муж.') else PATRONYMICS_FEMALE_S
            )

        dset = gen_persons(
            age, sex, amount, lastnames, firstnames, patronymics
        )

        base_dset.extend(dset)

    random.shuffle(base_dset)

    return base_dset


def gen_persons(
    age: Age,
    sex: str,
    amount: int,
    lastnames: dict[str, float],
    firstnames: dict[str, float],
    patronymics: dict[str, float],
) -> list[list[str]]:
    """Generate fake Russian data (name, sex, date of birth).

    Args:
        age: An object of dataclass 'Age' for a certain age.
        sex: A value(str) from namedtuple 'Sex'.
        amount: An amount (int) of male/female persons of a certain age.
        lastnames: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).
        firstnames: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).
        patronymics: A Russian last names (dict) mapping names(keys, str) and
        their weights (values, float).

    Returns:
        A list (of lists of str) containing fake Russan personal data (name,
        sex, date of birth) of a certain sex and age.
    """
    persons_lst: list[list[str]] = []
    birthdays_dq = deque(birthdays.gen_birthdays(age, amount))

    lastnames_dq = deque(reader.read_names(amount, lastnames))
    firstnames_dq = deque(reader.read_names(amount, firstnames))
    patronymics_dq = deque(reader.read_names(amount, patronymics))

    for i in range(amount):
        birthday = birthdays_dq.popleft()

        person = [
            lastnames_dq.popleft(),
            firstnames_dq.popleft(),
            patronymics_dq.popleft(),
            sex,
            birthday,
        ]

        if birthdays_dq.count(birthday) > 0:
            while persons_lst.count(person) > 0:
                birthdays_dq.append(person.pop())
                birthday_new = birthdays_dq.popleft()
                person.append(birthday_new)

        persons_lst.append(person)

    return persons_lst


def gen_contacts(total: int, base_dset: list[list[str]]) -> zip:
    """Generate a dataset of fake Russian contacts (cell phone numbers, emails).

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        base_dset: A dataset (list of lists of str) containing fake Russian
        personal data, including names and date of birth.

    Returns:
        A zipped tupple aggregating lists (of str) with fake Russian phones
        and emails.
    """
    phones_lst = phones.gen_phones(total)
    emails_lst = emails.gen_emails(base_dset)

    contacts_dset = zip(phones_lst, emails_lst)

    return contacts_dset


def gen_locations(
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
    regions_lst: list[str] = []
    localities_lst: list[str] = []

    locations_lst = reader.read_locations(total, localities_dict)

    for location in locations_lst:
        regions_lst.append(location[0])
        localities_lst.append(location[1])

    locations_dset = zip(regions_lst, localities_lst)

    return locations_dset

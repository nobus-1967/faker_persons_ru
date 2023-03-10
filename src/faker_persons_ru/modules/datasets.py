"""
Module for generating datasets (fake Russian persons, contacts and locations).
"""
import random

from itertools import product

from faker_persons_ru.modules import demography
from faker_persons_ru.modules.demography import Age, SEX
from faker_persons_ru.modules.demography import JUNIOR, MIDDLE, SENIOR
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
    """Generate a dataset of fake Russian persons (name, sex, date of birth).

    Args:
        total: int - A total amount of fake personal records; from user input.

    Returns:
        A list (lists of str) containing fake Russian personal data.
    """
    # 1. Calculate age and sex values.
    total_j, total_m, total_s = demography.calc_ages(total)

    total_male_j, total_female_j = demography.calc_sex(total_j, JUNIOR.female)
    total_male_m, total_female_m = demography.calc_sex(total_m, MIDDLE.female)
    total_male_s, total_female_s = demography.calc_sex(total_s, SENIOR.female)

    total_male = total_male_j + total_male_m + total_male_s
    total_female = total_female_j + total_female_m + total_female_s

    amounts_lst = [
        total_male_j,
        total_female_j,
        total_male_m,
        total_female_m,
        total_male_s,
        total_female_s,
    ]

    demography_lst = list(
        product([JUNIOR, MIDDLE, SENIOR], [SEX.male, SEX.female])
    )

    # 2. Create lists of names.
    lastnames_male = reader.read_names(total_male, LASTNAMES_MALE)
    lastnames_female = reader.read_names(total_female, LASTNAMES_FEMALE)
    firstnames_male_j = reader.read_names(total_male_j, FIRSTNAMES_MALE_J)
    firstnames_female_j = reader.read_names(
        total_female_j, FIRSTNAMES_FEMALE_J
    )
    firstnames_male_m = reader.read_names(total_male_m, FIRSNAMES_MALE_M)
    firstnames_female_m = reader.read_names(total_female_m, FIRSNAMES_FEMALE_M)
    firstnames_male_s = reader.read_names(total_male_s, FIRSNAMES_MALE_S)
    firstnames_female_s = reader.read_names(total_female_s, FIRSNAMES_FEMALE_S)
    patronymics_male_j = reader.read_names(total_male_j, PATRONYMICS_MALE_J)
    patronymics_female_j = reader.read_names(
        total_female_j, PATRONYMICS_FEMALE_J
    )
    patronymics_male_m = reader.read_names(total_male_m, PATRONYMICS_MALE_M)
    patronymics_female_m = reader.read_names(
        total_female_m, PATRONYMICS_FEMALE_M
    )
    patronymics_male_s = reader.read_names(total_male_s, PATRONYMICS_MALE_S)
    patronymics_female_s = reader.read_names(
        total_female_s, PATRONYMICS_FEMALE_S
    )

    # 3. Generate dataset.
    base_dset = []

    for i, part in enumerate(demography_lst):
        age, sex = part
        amount = amounts_lst[i]

        lastnames = lastnames_male if (sex == 'муж.') else lastnames_female
        if age.group == 'J':
            firstnames = (
                firstnames_male_j if (sex == 'муж.') else firstnames_female_j
            )
            patronymics = (
                patronymics_male_j if (sex == 'муж.') else patronymics_female_j
            )
        if age.group == 'M':
            firstnames = (
                firstnames_male_m if (sex == 'муж.') else firstnames_female_m
            )
            patronymics = (
                patronymics_male_m if (sex == 'муж.') else patronymics_female_m
            )
        if age.group == 'S':
            firstnames = (
                firstnames_male_s if (sex == 'муж.') else firstnames_female_s
            )
            patronymics = (
                patronymics_male_s if (sex == 'муж.') else patronymics_female_s
            )

        dset = gen_persons(
            age, sex, amount, lastnames, firstnames, patronymics
        )

        base_dset += dset

    random.shuffle(base_dset)

    return base_dset


def gen_persons(
    age: Age,
    sex: str,
    amount: int,
    lastnames: list[str],
    firstnames: list[str],
    patronymics: list[str],
) -> list[list[str]]:
    """Generate fake Russian data for a certain age (name, sex, date of birth).

    Args:
        age: object - An object of dataclass 'Age' (certain age).
        sex: str - A value from namedtuple 'Sex' (male/female).
        amount: int - An amount of male/female persons of a certain age.
        lastnames: list of str - Russian last names for male/female.
        firstnames: list of str - Russian first names of male/female of a
        certain age.
        patronymics: list of str - Russian patronymics of male/female of a
        certain age.

    Returns:
        A list (lists of str) containing fake Russan personal data of a certain
        sex and age.
    """
    persons_lst = []
    # List of birthdays for uniqueness check.
    birthdays = []
    totals = amount

    while totals > 0:
        birthday = age.gen_birthday()

        while birthday in birthdays:
            birthday = age.gen_birthday()
        birthdays.append(birthday)

        person = [
            lastnames.pop(),
            firstnames.pop(),
            patronymics.pop(),
            sex,
            birthday,
        ]

        persons_lst.append(person)
        totals -= 1

    return persons_lst


def gen_contacts(total: int, base_dset: list[list[str]]) -> zip:
    """Generate a dataset of fake Russian contacts (cell phone numbers, emails).

    Args:
        total: int - A total amount of fake personal records; from user input.
        base_dset: list (lists of str) - Fake Russian personal data.

    Returns:
        A zip of lists (str) containing fake Russian phone numbers and email
        addresses.
    """
    phones_lst = phones.gen_phones(total)
    emails_lst = emails.gen_emails(base_dset)

    contacts_dset = zip(phones_lst, emails_lst)

    return contacts_dset


def gen_locations(
    total: int, locations_dict: dict[str, tuple[str, float]]
) -> zip:
    """Generate a dataset of Russian locations (region and populated locality).

    Args:
        total: int - A total amount of fake personal records; from user input.
        locations_dict: dict - Russian localities (keys, str), regions and
        weights (values, tuple of str and float).

    Returns:
        A zip of lists (str) containing Russian regions and localities.
    """
    regions_lst = []
    localities_lst = []

    locations_lst = reader.read_locations(total, locations_dict)

    for location in locations_lst:
        regions_lst.append(location[0])
        localities_lst.append(location[1])

    locations_dset = zip(regions_lst, localities_lst)

    return locations_dset

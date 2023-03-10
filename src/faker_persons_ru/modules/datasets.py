"""
Module for generating datasets (fake Russian persons, contacts and locations).
"""
import random

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
    """Generate a dataset of fake Russian persons (name, sex, date of birth).

    Args:
        total: int - A total amount of fake personal records; from user input.

    Returns:
        A list (lists of str) containing fake Russian personal data.
    """
    # 1. Calculate age and sex values.
    amount_j, amount_m, amount_s = demography.calc_ages(total)

    amount_males_j, amount_females_j = demography.calc_sex(
        amount_j, JUNIOR.females
    )
    amount_males_m, amount_females_m = demography.calc_sex(
        amount_m, MIDDLE.females
    )
    amount_males_s, amount_females_s = demography.calc_sex(
        amount_s, SENIOR.females
    )

    amount_males = amount_males_j + amount_males_m + amount_males_s
    amount_females = amount_females_j + amount_females_m + amount_females_s

    amounts_lst = [
        amount_males_j,
        amount_females_j,
        amount_males_m,
        amount_females_m,
        amount_males_s,
        amount_females_s,
    ]

    demography_lst = list(
        product([JUNIOR, MIDDLE, SENIOR], [SEX.male, SEX.female])
    )

    # 2. Create lists of names.
    lastnames_male = reader.read_names(amount_males, LASTNAMES_MALE)
    lastnames_female = reader.read_names(amount_females, LASTNAMES_FEMALE)
    firstnames_males_j = reader.read_names(amount_males_j, FIRSTNAMES_MALE_J)
    firstnames_females_j = reader.read_names(
        amount_females_j, FIRSTNAMES_FEMALE_J
    )
    firstnames_males_m = reader.read_names(amount_males_m, FIRSNAMES_MALE_M)
    firstnames_females_m = reader.read_names(
        amount_females_m, FIRSNAMES_FEMALE_M
    )
    firstnames_males_s = reader.read_names(amount_males_s, FIRSNAMES_MALE_S)
    firstnames_females_s = reader.read_names(
        amount_females_s, FIRSNAMES_FEMALE_S
    )
    patronymics_males_j = reader.read_names(amount_males_j, PATRONYMICS_MALE_J)
    patronymics_females_j = reader.read_names(
        amount_females_j, PATRONYMICS_FEMALE_J
    )
    patronymics_males_m = reader.read_names(amount_males_m, PATRONYMICS_MALE_M)
    patronymics_females_m = reader.read_names(
        amount_females_m, PATRONYMICS_FEMALE_M
    )
    patronymics_males_s = reader.read_names(amount_males_s, PATRONYMICS_MALE_S)
    patronymics_females_s = reader.read_names(
        amount_females_s, PATRONYMICS_FEMALE_S
    )

    # 3. Generate dataset.
    base_dset: list[list[str]] = []

    for i, part in enumerate(demography_lst):
        age, sex = part
        amount = amounts_lst[i]

        lastnames = lastnames_male if (sex == 'муж.') else lastnames_female
        if age.group == 'J':
            firstnames = (
                firstnames_males_j if (sex == 'муж.') else firstnames_females_j
            )
            patronymics = (
                patronymics_males_j
                if (sex == 'муж.')
                else patronymics_females_j
            )
        if age.group == 'M':
            firstnames = (
                firstnames_males_m if (sex == 'муж.') else firstnames_females_m
            )
            patronymics = (
                patronymics_males_m
                if (sex == 'муж.')
                else patronymics_females_m
            )
        if age.group == 'S':
            firstnames = (
                firstnames_males_s if (sex == 'муж.') else firstnames_females_s
            )
            patronymics = (
                patronymics_males_s
                if (sex == 'муж.')
                else patronymics_females_s
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
    persons_lst: list[list[str]] = []
    birthdays_lst = birthdays.gen_birthdays(age, amount)

    for _ in range(amount):
        birthday = birthdays_lst.pop()

        person = [
            lastnames.pop(),
            firstnames.pop(),
            patronymics.pop(),
            sex,
            birthday,
        ]

        if birthdays_lst.count(birthday) > 0:
            while persons_lst.count(person) > 0:
                birthdays_lst.insert(0, person.pop())
                birthday_new = birthdays_lst.pop()
                person.append(birthday_new)

        persons_lst.append(person)

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
    regions_lst: list[str] = []
    localities_lst: list[str] = []

    locations_lst = reader.read_locations(total, locations_dict)

    for location in locations_lst:
        regions_lst.append(location[0])
        localities_lst.append(location[1])

    locations_dset = zip(regions_lst, localities_lst)

    return locations_dset

"""Module for generating datasets (fake Russian personal data and contacts)."""
import random

from pathlib import Path

from faker_persons_ru.modules import demography
from faker_persons_ru.modules.demography import Age, SEX
from faker_persons_ru.modules.demography import JUNIOR, MIDDLE, SENIOR
from faker_persons_ru.modules import emails
from faker_persons_ru.modules import phones
from faker_persons_ru.data import names
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


def generate_persons(total: int) -> list[list[str]]:
    """Generate a dataset of fake Russian data (name, sex, date of birth).

    Args:
        total: integer - total amount of persons from user input.

    Returns:
        list of lists (containing strings) with fake Russian personal
    """
    # 1. Calculate age and sex values.
    amounts = list()

    total_j, total_m, total_s = demography.calc_ages(total)

    total_male_j, total_female_j = demography.calc_sex(total_j, JUNIOR.female)
    amounts.extend([total_male_j, total_female_j])
    total_male_m, total_female_m = demography.calc_sex(total_m, MIDDLE.female)
    amounts.extend([total_male_m, total_female_m])
    total_male_s, total_female_s = demography.calc_sex(total_s, SENIOR.female)
    amounts.extend([total_male_s, total_female_s])

    total_male = total_male_j + total_male_m + total_male_s
    total_female = total_female_j + total_female_m + total_female_s

    groups = list()

    for i, age in enumerate([JUNIOR, MIDDLE, SENIOR]):
        for sex in [SEX.male, SEX.female]:
            groups.append([age, sex])
    for i, group in enumerate(groups):
        group.append(amounts[i])

    # 2. Create lists of names.
    lastnames_male = names.read_names(total_male, LASTNAMES_MALE)
    lastnames_female = names.read_names(total_female, LASTNAMES_FEMALE)
    firstnames_male_j = names.read_names(total_male_j, FIRSTNAMES_MALE_J)
    firstnames_female_j = names.read_names(total_female_j, FIRSTNAMES_FEMALE_J)
    firstnames_male_m = names.read_names(total_male_m, FIRSNAMES_MALE_M)
    firstnames_female_m = names.read_names(total_female_m, FIRSNAMES_FEMALE_M)
    firstnames_male_s = names.read_names(total_male_s, FIRSNAMES_MALE_S)
    firstnames_female_s = names.read_names(total_female_s, FIRSNAMES_FEMALE_S)
    patronymics_male_j = names.read_names(total_male_j, PATRONYMICS_MALE_J)
    patronymics_female_j = names.read_names(
        total_female_j, PATRONYMICS_FEMALE_J
    )
    patronymics_male_m = names.read_names(total_male_m, PATRONYMICS_MALE_M)
    patronymics_female_m = names.read_names(
        total_female_m, PATRONYMICS_FEMALE_M
    )
    patronymics_male_s = names.read_names(total_male_s, PATRONYMICS_MALE_S)
    patronymics_female_s = names.read_names(
        total_female_s, PATRONYMICS_FEMALE_S
    )

    # 3. Generate dataset.
    dataset_persons = list()

    for group in groups:
        age, sex, amount = group

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

        dataset = generate_data(
            age, sex, amount, lastnames, firstnames, patronymics
        )

        dataset_persons += dataset

    random.shuffle(dataset_persons)

    return dataset_persons


def generate_data(
    age: Age,
    sex: str,
    amount: int,
    lastnames: list[str],
    firstnames: list[str],
    patronymics: list[str],
) -> list[list[str]]:
    """Generate fake Russian data for a certain age (name, sex, date of birth).

    Args:
        age: object - object of dataclass 'Age' (certain age).
        sex: string - value from namedtuple 'Sex' (male/female).
        amount: integer - amount of male/female persons of a certain age.
        lastnames: list - Russian last names for male/female.
        firstnames: list - Russian first names of male/female of a certain age.
        patronymics: list - Russian patronymics of male/female of a certain
        age.

    Returns:
        list of lists (containing strings) with fake Russan personal data of
        a certain sex and age.
    """
    persons = [None] * amount
    # For a unique birthday check: list of birthdays.
    birthdays = [None] * amount
    totals = amount

    while totals > 0:
        lastname = lastnames.pop()
        firstname = firstnames.pop()
        patronymic = patronymics.pop()

        birthday = age.generate_birthday()

        while birthday in birthdays:
            birthday = age.generate_birthday()
        birthdays[totals - 1] = birthday

        person = [lastname, firstname, patronymic, sex, birthday]

        persons[totals - 1] = person
        totals -= 1

    return persons


def generate_contacts(total: int, dataset_persons: list[list[str]]) -> zip:
    """Generate a dataset of fake Russian contacts (cell phone numbers, emails).

    Args:
        total: integer - total amount of persons from user input.
        dataset_persons: list of lists (containing strings) - fake Russian
        personal

    Returns:
        zip of lists (containing strings) with fake Russian phones and emails.
    """
    phone_nums = phones.generate_phones(total)
    email_addresses = emails.generate_emails(dataset_persons)

    dataset_contacts = zip(phone_nums, email_addresses)

    return dataset_contacts
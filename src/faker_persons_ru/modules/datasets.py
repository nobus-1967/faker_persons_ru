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
    total_j, total_m, total_s = demography.calc_ages(total)
    total_male_j, total_female_j = demography.calc_sex(total_j, JUNIOR.female)
    total_male_m, total_female_m = demography.calc_sex(total_m, MIDDLE.female)
    total_male_s, total_female_s = demography.calc_sex(total_s, SENIOR.female)
    total_male = total_male_j + total_male_m + total_male_s
    total_female = total_female_j + total_female_m + total_female_s

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
    dataset_male_j = generate_data(
        JUNIOR,
        SEX.male,
        total_male_j,
        lastnames_male,
        firstnames_male_j,
        patronymics_male_j,
    )
    dataset_female_j = generate_data(
        JUNIOR,
        SEX.female,
        total_female_j,
        lastnames_female,
        firstnames_female_j,
        patronymics_female_j,
    )
    dataset_male_m = generate_data(
        MIDDLE,
        SEX.male,
        total_male_m,
        lastnames_male,
        firstnames_male_m,
        patronymics_male_m,
    )
    dataset_female_m = generate_data(
        MIDDLE,
        SEX.female,
        total_female_m,
        lastnames_female,
        firstnames_female_m,
        patronymics_female_m,
    )
    dataset_male_s = generate_data(
        SENIOR,
        SEX.male,
        total_male_s,
        lastnames_male,
        firstnames_male_s,
        patronymics_male_s,
    )
    dataset_female_s = generate_data(
        SENIOR,
        SEX.female,
        total_female_s,
        lastnames_female,
        firstnames_female_s,
        patronymics_female_s,
    )

    dataset_persons = (
        dataset_male_j
        + dataset_female_j
        + dataset_male_m
        + dataset_female_m
        + dataset_male_s
        + dataset_female_s
    )
    random.shuffle(dataset_persons)

    return dataset_persons


def generate_data(
    age: Age,
    sex: str,
    total_sex_age: int,
    lastnames: list[str],
    firstnames: list[str],
    patronymics: list[str],
) -> list[list[str]]:
    """Generate fake Russian data for a certain age (name, sex, date of birth).

    Args:
        age: object - object of dataclass 'Age' (certain age).
        sex: string - value from namedtuple 'Sex' (male/female).
        total_sex_age: integer - amount of male/female persons of a certain age.
        lastnames: list - Russian last names for male/female.
        firstnames: list - Russian first names of male/age of a certain age.
        patronymics: list - Russian patronymics of male/age of a certain age.

    Returns:
        list of lists (containing strings) with fake Russan personal data of
        a certain sex and age.
    """
    persons = list()
    # For a unique birthday check: list of birthdays.
    birthdays = list()
    totals = total_sex_age

    while totals > 0:
        lastname = lastnames.pop()
        firstname = firstnames.pop()
        patronymic = patronymics.pop()

        birthday = age.generate_birthday()

        while birthday in birthdays:
            birthday = age.generate_birthday()
        birthdays.append(birthday)

        person = [lastname, firstname, patronymic, sex, birthday]

        persons.append(person)
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

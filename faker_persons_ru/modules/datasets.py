"""Module for generating basic dataset (fake persons and their contacts)."""
import random

from modules.demography import Age, JUNIOR, MIDDLE, SENIOR, SEX
from modules.demography import calc_ages, calc_sex
from modules.emails import generate_emails
from modules.names import read_names
from modules.phones import generate_phones


def generate_persons(total: int) -> list[list[str]]:
    """Generate a dataset of fake persons (name, sex, date of birth).

    Args:
        total: integer of total persons from user input.

    Returns:
        list of lists (containing strings) with fake personal info.
    """
    # 1. Calculate age and sex values.
    total_j, total_m, total_s = calc_ages(total)
    total_male_j, total_female_j = calc_sex(total_j, JUNIOR.female)
    total_male_m, total_female_m = calc_sex(total_m, MIDDLE.female)
    total_male_s, total_female_s = calc_sex(total_s, SENIOR.female)
    total_male = total_male_j + total_male_m + total_male_s
    total_female = total_female_j + total_female_m + total_female_s

    # 2. Create lists of names.
    lastnames_male = read_names(total_male, 'sources/lastnames_male.csv')
    lastnames_female = read_names(total_female, 'sources/lastnames_female.csv')
    firstnames_male_j = read_names(
        total_male_j, 'sources/firstnames_junior_male.csv'
    )
    firstnames_female_j = read_names(
        total_female_j, 'sources/firstnames_junior_female.csv'
    )
    firstnames_male_m = read_names(
        total_male_m, 'sources/firstnames_middle_male.csv'
    )
    firstnames_female_m = read_names(
        total_female_m, 'sources/firstnames_middle_female.csv'
    )
    firstnames_male_s = read_names(
        total_male_s, 'sources/firstnames_senior_male.csv'
    )
    firstnames_female_s = read_names(
        total_female_s, 'sources/firstnames_senior_female.csv'
    )
    patronymics_male_j = read_names(
        total_male_j, 'sources/patronymics_junior_male.csv'
    )
    patronymics_female_j = read_names(
        total_female_j, 'sources/patronymics_junior_female.csv'
    )
    patronymics_male_m = read_names(
        total_male_m, 'sources/patronymics_middle_male.csv'
    )
    patronymics_female_m = read_names(
        total_female_m, 'sources/patronymics_middle_female.csv'
    )
    patronymics_male_s = read_names(
        total_male_s, 'sources/patronymics_senior_male.csv'
    )
    patronymics_female_s = read_names(
        total_female_s, 'sources/patronymics_senior_female.csv'
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
    """Generate fake persons of certain age (name, sex, date of birth).

    Args:
        age: object of dataclass for certain age.
        sex: string as certain value of namedtuple.
        total_sex_age: integer for an amount of male/female persons of certain
        age.
        lastnames: list of last names for male/female.
        firstnames: list of first names of male/age of certain age.
        patronymics: list of patronymics of male/age of certain age.

    Returns:
        list of lists (containing strings) with fake personal of certain sex
        and age.
    """
    persons = list()
    birthdays = list()  # For a unique phone number check.
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
    """Generate a dataset of fake contacts (phone, email).

    Args:
        total: integer of total persons from user input.
        dataset_persons: list of lists (containing strings) with fake personal info.

    Returns:
        list of lists (containing strings) with fake phones and emails.
    """
    phones = generate_phones(total)
    emails = generate_emails(dataset_persons)

    dataset_contacts = zip(phones, emails)

    return dataset_contacts

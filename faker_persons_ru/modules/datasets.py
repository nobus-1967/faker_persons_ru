"""Module for generating datasets (fake Russian personal data and contacts)."""
import random

from pathlib import Path

import modules.demography
import modules.emails
import modules.names
import modules.phones


def generate_persons(total: int) -> list[list[str]]:
    """Generate a dataset of fake Russian data (name, sex, date of birth).

    Args:
        total: integer - total amount of persons from user input.

    Returns:
        list of lists (containing strings) with fake Russian personal data.
    """
    # 1. Calculate age and sex values.
    total_j, total_m, total_s = modules.demography.calc_ages(total)
    total_male_j, total_female_j = modules.demography.calc_sex(
        total_j, modules.demography.JUNIOR.female
    )
    total_male_m, total_female_m = modules.demography.calc_sex(
        total_m, modules.demography.MIDDLE.female
    )
    total_male_s, total_female_s = modules.demography.calc_sex(
        total_s, modules.demography.SENIOR.female
    )
    total_male = total_male_j + total_male_m + total_male_s
    total_female = total_female_j + total_female_m + total_female_s

    # 2. Create lists of names.
    data = Path.cwd().joinpath('data')

    lastnames_male = modules.names.read_names(
        total_male, data.joinpath('lastnames_male.csv')
    )
    lastnames_female = modules.names.read_names(
        total_female, data.joinpath('lastnames_female.csv')
    )
    firstnames_male_j = modules.names.read_names(
        total_male_j, data.joinpath('firstnames_junior_male.csv')
    )
    firstnames_female_j = modules.names.read_names(
        total_female_j, data.joinpath('firstnames_junior_female.csv')
    )
    firstnames_male_m = modules.names.read_names(
        total_male_m, data.joinpath('firstnames_middle_male.csv')
    )
    firstnames_female_m = modules.names.read_names(
        total_female_m, data.joinpath('firstnames_middle_female.csv')
    )
    firstnames_male_s = modules.names.read_names(
        total_male_s, data.joinpath('firstnames_senior_male.csv')
    )
    firstnames_female_s = modules.names.read_names(
        total_female_s, data.joinpath('firstnames_senior_female.csv')
    )
    patronymics_male_j = modules.names.read_names(
        total_male_j, data.joinpath('patronymics_junior_male.csv')
    )
    patronymics_female_j = modules.names.read_names(
        total_female_j, data.joinpath('patronymics_junior_female.csv')
    )
    patronymics_male_m = modules.names.read_names(
        total_male_m, data.joinpath('patronymics_middle_male.csv')
    )
    patronymics_female_m = modules.names.read_names(
        total_female_m, data.joinpath('patronymics_middle_female.csv')
    )
    patronymics_male_s = modules.names.read_names(
        total_male_s, data.joinpath('patronymics_senior_male.csv')
    )
    patronymics_female_s = modules.names.read_names(
        total_female_s, data.joinpath('patronymics_senior_female.csv')
    )

    # 3. Generate dataset.
    dataset_male_j = generate_data(
        modules.demography.JUNIOR,
        modules.demography.SEX.male,
        total_male_j,
        lastnames_male,
        firstnames_male_j,
        patronymics_male_j,
    )
    dataset_female_j = generate_data(
        modules.demography.JUNIOR,
        modules.demography.SEX.female,
        total_female_j,
        lastnames_female,
        firstnames_female_j,
        patronymics_female_j,
    )
    dataset_male_m = generate_data(
        modules.demography.MIDDLE,
        modules.demography.SEX.male,
        total_male_m,
        lastnames_male,
        firstnames_male_m,
        patronymics_male_m,
    )
    dataset_female_m = generate_data(
        modules.demography.MIDDLE,
        modules.demography.SEX.female,
        total_female_m,
        lastnames_female,
        firstnames_female_m,
        patronymics_female_m,
    )
    dataset_male_s = generate_data(
        modules.demography.SENIOR,
        modules.demography.SEX.male,
        total_male_s,
        lastnames_male,
        firstnames_male_s,
        patronymics_male_s,
    )
    dataset_female_s = generate_data(
        modules.demography.SENIOR,
        modules.demography.SEX.female,
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
    age: modules.demography.Age,
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
        personal data.

    Returns:
        zip of lists (containing strings) with fake Russian phones and emails.
    """
    phones = modules.phones.generate_phones(total)
    emails = modules.emails.generate_emails(dataset_persons)

    dataset_contacts = zip(phones, emails)

    return dataset_contacts

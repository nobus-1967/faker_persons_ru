#!/usr/bin/env python3
"""
Main module for:
- set options through CLI,
- create resulting DataFrames of fake Russian personal data, contacts and
locations, and
- save data into different formats (CSV, SQL, MS Excel) in user home directory.
"""
import click
import pandas as pd

from pathlib import Path

from faker_persons_ru.modules import datasets
from faker_persons_ru.modules import outputs
from faker_persons_ru.data.locations import LOCALITIES
from faker_persons_ru import __version__

PATH_TO_OUTPUT: Path = Path.home()
PERSONS: tuple[str, str, str, str, str] = (
    'Фамилия',
    'Имя',
    'Отчество',
    'Пол',
    'Дата рождения',
)
CONTACTS: tuple[str, str] = ('Телефон', 'E-mail')
LOCATIONS: tuple[str, str] = ('Регион', 'Населённый пункт')


@click.command()
@click.option(
    '-t',
    '--total',
    type=click.IntRange(1, 10_000, clamp=True),
    default=1_000,
    help=(
        'Number of generating fake personal data (default 1000).'
        + ' Only one value is accepted!'
    ),
)
@click.option(
    '-d',
    '--data',
    type=click.Choice(
        ['base', 'contacts', 'locations', 'full'], case_sensitive=False
    ),
    multiple=False,
    help=(
        'Generated data: "base" as default (full name, sex, date of birth), '
        + '"contacts" ("base" + cell phone number and email address), '
        + '"locations" ("base" + region and locality) or "full".'
        + ' Only one value is accepted!'
    ),
)
@click.option(
    '-f',
    '--filetype',
    type=click.Choice(['csv', 'sql', 'sqlite3', 'xlsx'], case_sensitive=False),
    multiple=True,
    help=(
        'Type of output file: CSV, Common SQL, SQLite3 DB, MS Excel.'
        + ' Multiply values are accepted!'
    ),
)
@click.option(
    '-o',
    '--output',
    type=click.Path(),
    default='new_dataset',
    prompt=True,
    prompt_required=False,
    help=(
        "Output filename, no extension required (default 'new_dataset')."
        + ' Only one value is accepted!'
    ),
)
def main(
    total: int, filetype: tuple[str, ...], data: str, output: str
) -> None:
    """
    faker_persons_ru (using Click and pandas) generates datasets of fake Russian
    personal data (full name, sex, phone number, email address, region and
    locality) and store them into different formats.
    """
    click.secho(
        f'Generating new dataset "{output}", waiting a few seconds...\n',
        fg='green',
    )

    dataset_persons = datasets.generate_persons(total)
    indeces: pd.RangeIndex = pd.RangeIndex(start=1, stop=total + 1, name='ID')
    df_personal = pd.DataFrame(dataset_persons, columns=PERSONS, index=indeces)

    if data == 'contacts':
        dataset_contacts = datasets.generate_contacts(total, dataset_persons)
        df_contacts = pd.DataFrame(
            dataset_contacts, columns=CONTACTS, index=indeces
        )

        df = df_personal.join(df_contacts)
    elif data == 'locations':
        dataset_locations = datasets.generate_locations(total, LOCALITIES)
        df_locations = pd.DataFrame(
            dataset_locations, columns=LOCATIONS, index=indeces
        )

        df = df_personal.join(df_locations)
    elif data == 'full':
        dataset_contacts = datasets.generate_contacts(total, dataset_persons)
        df_contacts = pd.DataFrame(
            dataset_contacts, columns=CONTACTS, index=indeces
        )

        dataset_locations = datasets.generate_locations(total, LOCALITIES)
        df_locations = pd.DataFrame(
            dataset_locations, columns=LOCATIONS, index=indeces
        )

        df = df_personal.join([df_contacts, df_locations])
    else:
        df = df_personal

    click.echo(df)

    if 'csv' in filetype:
        outputs.generate_csv(df, output, PATH_TO_OUTPUT)
    if 'sql' in filetype:
        outputs.generate_sql(df, output, PATH_TO_OUTPUT)
    if 'sqlite3' in filetype:
        outputs.generate_sqlite3(df, output, PATH_TO_OUTPUT)
    if 'xlsx' in filetype:
        outputs.generate_excel(df, output, PATH_TO_OUTPUT)

    click.echo()

    for extension in filetype:
        click.echo(
            f'Dataset "{output}.{filetype}" ({total} personal data records) '
            + f'was successfully stored in your "{PATH_TO_OUTPUT}" directory.'
        )

    click.secho(
        '----------------------------\n'
        + f'(c) Anatoly Shcherbina, 2023\n'
        + f'faker_persons_ru, ver. {__version__.__version__}',
        fg='blue',
    )


if __name__ == '__main__':
    main()

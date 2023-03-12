#!/usr/bin/env python3
"""
Main module for:
- define options through CLI,
- set type of generating fake Russian personal data,
- create resulting DataFrames of fake Russian personal data, and
- save data into different formats (CSV, Common SQL, SQLite3 or MS Excel) in
user's home directory.
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
    type=click.IntRange(1, 100_000, clamp=True),
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
def cli(total: int, filetype: tuple[str, ...], data: str, output: str) -> None:
    """
    faker_persons_ru (using Click and pandas) generates datasets of fake Russian
    personal data (full name, sex, phone number, email address, region and
    locality) and store them into different formats.
    """
    click.secho(
        f'Generating new dataset "{output}", waiting a few seconds...\n',
        fg='green',
    )

    df = gen_data(total, data)
    click.echo(df)

    if 'csv' in filetype:
        outputs.to_csv(df, output, PATH_TO_OUTPUT)
    if 'sql' in filetype:
        outputs.to_sql(df, output, PATH_TO_OUTPUT)
    if 'sqlite3' in filetype:
        outputs.to_sqlite3(df, output, PATH_TO_OUTPUT)
    if 'xlsx' in filetype:
        outputs.to_excel(df, output, PATH_TO_OUTPUT)

    click.echo()

    for extension in filetype:
        click.echo(
            f'The dataset "{output}.{extension}" '
            + f'({total} fake personal data records) '
            + f'was successfully stored in your "{PATH_TO_OUTPUT}" directory.'
        )

    click.secho(
        '----------------------------\n'
        + f'(c) Anatoly Shcherbina, 2023\n'
        + f'faker_persons_ru, ver. {__version__.__version__}',
        fg='blue',
    )


def gen_data(total: int, data: str) -> pd.DataFrame:
    """Create pandas DataFrame frome generated dataset(s).

    Args:
        total: A total amount (int) of records/fake persons; from user input.
        data: A type (str) of generated data - personal info/
        personal info and contacts/personal info and localities/full info.

    Returns:
        A pandas DataFrame containing fake Russian personal data and--if they
        were chosen--contacts info and locations.
    """
    base_dset = datasets.gen_base(total)
    indeces: pd.RangeIndex = pd.RangeIndex(start=1, stop=total + 1, name='ID')
    base_df = pd.DataFrame(base_dset, columns=PERSONS, index=indeces)

    if data == 'contacts':
        contacts_dset = datasets.gen_contacts(total, base_dset)
        contacts_df = pd.DataFrame(
            contacts_dset, columns=CONTACTS, index=indeces
        )
        base_plus_contacts_df = base_df.join(contacts_df)

        return base_plus_contacts_df
    elif data == 'locations':
        locations_dset = datasets.gen_locations(total, LOCALITIES)
        locations_df = pd.DataFrame(
            locations_dset, columns=LOCATIONS, index=indeces
        )
        base_plus_locations_df = base_df.join(locations_df)

        return base_plus_locations_df
    elif data == 'full':
        contacts_dset = datasets.gen_contacts(total, base_dset)
        contacts_df = pd.DataFrame(
            contacts_dset, columns=CONTACTS, index=indeces
        )

        locations_dset = datasets.gen_locations(total, LOCALITIES)
        locations_df = pd.DataFrame(
            locations_dset, columns=LOCATIONS, index=indeces
        )

        full_df = base_df.join([contacts_df, locations_df])

        return full_df
    else:
        return base_df


if __name__ == '__main__':
    cli()

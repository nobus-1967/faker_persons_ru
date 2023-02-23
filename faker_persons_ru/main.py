#!/usr/bin/env python3
"""
Main module for:
- set options through CLI,
- create resulting DataFrames of fake Russian personal data and contacts, and
- save data into different formats (CSV, SQL, MS Excel) in user home directory.
"""
import click
import pandas as pd

from pathlib import Path

import modules.datasets
import modules.outputs
import __version__

PATH_TO_OUTPUT: Path = Path.home()
PERSONS: tuple[str, str, str, str, str] = (
    'Фамилия',
    'Имя',
    'Отчество',
    'Пол',
    'Дата рождения',
)
CONTACTS: tuple[str, str] = ('Телефон', 'E-mail')


@click.command()
@click.option(
    '-t',
    '--total',
    type=click.IntRange(1, 10_000),
    default=1_000,
    help='NUMBER of generating fake personal data (default 1000).',
)
@click.option(
    '-f',
    '--filetype',
    type=click.Choice(['csv', 'sql', 'sqlite3', 'xlsx'], case_sensitive=False),
    multiple=True,
    help=(
        'Type of output file: '
        + 'CSV, Common SQL, SQLite3 DB, MS Excel (default CSV).'
    ),
)
@click.option(
    '-o',
    '--output',
    default='new_dataset',
    type=click.Path(),
    help="Output FILENAME, no extension required (default 'new_dataset').",
)
def main(total: int, filetype: str, output: str) -> None:
    """faker_persons_ru (using Click and pandas):

    - Generate datasets of fake Russian personal data and store them.

    - Create pandas DataFrames  and store it as CSV, SQL, SQLite3 and Microsoft
    Excel files in users home directory.

    - Echo parts of DataFrames (and--if user entered filetype(s)--also echo
    results of storing files).
    """
    click.echo(
        f'Generating new dataset "{output}", waiting a few seconds...\n'
    )

    dataset_persons = modules.datasets.generate_persons(total)
    indexes: pd.RangeIndex = pd.RangeIndex(start=1, stop=total + 1, name='ID')
    df_persons = pd.DataFrame(dataset_persons, columns=PERSONS, index=indexes)

    dataset_contacts = modules.datasets.generate_contacts(
        total, dataset_persons
    )
    df_contacts = pd.DataFrame(
        dataset_contacts, columns=CONTACTS, index=indexes
    )

    df_full = df_persons.join(df_contacts)
    click.echo(df_full)

    if 'csv' in filetype:
        modules.outputs.generate_csv(df_full, output, PATH_TO_OUTPUT)
    if 'sql' in filetype:
        modules.outputs.generate_sql(
            df_persons, df_contacts, output, PATH_TO_OUTPUT
        )
    if 'sqlite3' in filetype:
        modules.outputs.generate_sqlite3(
            df_persons, df_contacts, output, PATH_TO_OUTPUT
        )
    if 'xlsx' in filetype:
        modules.outputs.generate_excel(df_full, output, PATH_TO_OUTPUT)

    click.echo()

    for filetype in filetype:
        click.echo(
            f'Dataset "{output}.{filetype}" ({total} personal data records) '
            + f'was successfully stored in your "{PATH_TO_OUTPUT}" directory.'
        )

    click.echo(
        '----------------------------\n'
        + f'(c) Anatoly Shcherbina, 2023\n'
        + f'faker_persons_ru, ver. {__version__.__version__}'
    )


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Main module for:
- set options through CLI,
- create resulting dataframes of fake persons and contacts and
- save results into files of different formats (CSV, SQL, MS Excel) in user
home directory.
"""
import click
import pandas as pd

from pathlib import Path

from modules.datasets import generate_persons, generate_contacts
from modules.outputs import (
    generate_csv,
    generate_sql,
    generate_sqlite3,
    generate_excel,
)

PATH: Path = Path.home()
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
    click.echo(
        f'Generating new dataset "{output}", waiting a few seconds...\n'
    )

    dataset_persons = generate_persons(total)
    indexes: pd.RangeIndex = pd.RangeIndex(start=1, stop=total + 1, name='ID')
    df_persons = pd.DataFrame(dataset_persons, columns=PERSONS, index=indexes)

    dataset_contacts = generate_contacts(total, dataset_persons)
    df_contacts = pd.DataFrame(
        dataset_contacts, columns=CONTACTS, index=indexes
    )

    df_full = df_persons.join(df_contacts)
    click.echo(df_full)

    if 'csv' in filetype:
        generate_csv(df_full, output, PATH)
    if 'sql' in filetype:
        generate_sql(df_persons, df_contacts, output, PATH)
    if 'sqlite3' in filetype:
        generate_sqlite3(df_persons, df_contacts, output, PATH)
    if 'xlsx' in filetype:
        generate_excel(df_full, output, PATH)

    click.echo()

    for filetype in filetype:
        click.echo(
            f'Dataset "{output}.{filetype}" ({total} personal data records) '
            + f'was successfully stored in your "{PATH}" directory.'
        )


if __name__ == '__main__':
    main()

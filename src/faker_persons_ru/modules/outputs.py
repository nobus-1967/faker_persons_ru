"""Module for generating output files (CSV, Common SQL, SQLite, MS Excel)."""
import csv
import sqlite3
import pandas as pd

from pathlib import Path

SQL_CREATE_PERSONS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS persons
    (
    ID INTEGER NOT NULL PRIMARY KEY,
    lastname TEXT NOT NULL,
    firstname TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    sex TEXT NOT NULL,
    date_of_birth DATE NOT NULL
    );
"""
SQL_CREATE_CONTACTS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS contacts
    (
    ID INTEGER NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
"""
SQL_CREATE_LOCATIONS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS locations
    (
    ID INTEGER NOT NULL,
    region TEXT NOT NULL,
    locality TEXT,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
"""
SQL_PERSONS_COLUMNS: list[str] = [
    'lastname',
    'firstname',
    'patronymic',
    'sex',
    'date_of_birth',
]
SQL_CONTACTS_COLUMNS: list[str] = ['phone', 'email']
SQL_LOCATIONS_COLUMNS: list[str] = ['region', 'locality']


def to_sql(
    df: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate a common SQL file (tables: 'persons', 'contacts', localities').

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save pandas DataFrames as a common SQL file (may be imported into RDBMS)
        using generic data types (TEXT for strings, DATE for dates).
    """
    filename = output + '.sql'
    filepath = path.joinpath(filename)

    is_contacts_info = 'Телефон' and 'E-mail' in df.columns
    is_locations_info = 'Регион' and 'Населённый пункт' in df.columns

    if is_contacts_info and is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contacts = df[['Телефон', 'E-mail']]
        locations = df[['Регион', 'Населённый пункт']]
    elif is_contacts_info and not is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contacts = df[['Телефон', 'E-mail']]
    elif not is_contacts_info and is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        locations = df[['Регион', 'Населённый пункт']]
    else:
        persons = df

    with open(filepath, 'w') as outfile:
        outfile.write(
            f'--- You have to create database manually and run this file!\n'
        )
        outfile.write('BEGIN TRANSACTION;\n')
        outfile.write(SQL_CREATE_PERSONS_TABLE)

        if is_contacts_info:
            outfile.write(SQL_CREATE_CONTACTS_TABLE)
        if is_contacts_info:
            outfile.write(SQL_CREATE_LOCATIONS_TABLE)

        for row in persons.itertuples():
            ID, lastname, firstname, patronymic, sex, date_of_birth = row
            outfile.write(
                'INSERT INTO persons VALUES '
                + f'({ID}, "{lastname}", "{firstname}", "{patronymic}", '
                + f'"{sex}", "{date_of_birth}");\n'
            )
        if is_contacts_info:
            for row in contacts.itertuples():
                ID, phone, email = row
                outfile.write(
                    'INSERT INTO contacts VALUES '
                    + f'({ID}, "{phone}", "{email}");\n'
                )
        if is_locations_info:
            for row in locations.itertuples():
                ID, region, locality = row
                outfile.write(
                    'INSERT INTO locations VALUES '
                    + f'({ID}, "{region}", "{locality}");\n'
                )

        outfile.write('\nCOMMIT;')


def to_sqlite3(
    df: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate a SQLite3 file (tables: 'persons', 'contacts', 'localities').

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save pandas DataFrames as a SQLIte3 database using generic data types
        (TEXT for strings, DATE for dates).
    """
    filename = output + '.sqlite3'
    filepath = path.joinpath(filename)
    if filepath.is_file():
        filepath.unlink()

    is_contacts_info = 'Телефон' and 'E-mail' in df.columns
    is_locations_info = 'Регион' and 'Населённый пункт' in df.columns

    if is_contacts_info and is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contacts = df[['Телефон', 'E-mail']]
        locations = df[['Регион', 'Населённый пункт']]
    elif is_contacts_info and not is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contacts = df[['Телефон', 'E-mail']]
    elif not is_contacts_info and is_locations_info:
        persons = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        locations = df[['Регион', 'Населённый пункт']]
    else:
        persons = df

    dict_replace_persons = {
        x: y for (x, y) in zip(persons.columns, SQL_PERSONS_COLUMNS)
    }
    persons = persons.rename(columns=dict_replace_persons)

    if is_contacts_info:
        dict_replace_contacts = {
            x: y for (x, y) in zip(contacts.columns, SQL_CONTACTS_COLUMNS)
        }
        contacts = contacts.rename(columns=dict_replace_contacts)
    if is_locations_info:
        dict_replace_locations = {
            x: y for (x, y) in zip(locations.columns, SQL_LOCATIONS_COLUMNS)
        }
        locations = locations.rename(columns=dict_replace_locations)

    con = sqlite3.connect(filepath)
    cur = con.cursor()

    cur.execute(SQL_CREATE_PERSONS_TABLE)

    if is_contacts_info:
        cur.execute(SQL_CREATE_CONTACTS_TABLE)
    if is_locations_info:
        cur.execute(SQL_CREATE_LOCATIONS_TABLE)

    persons.to_sql('persons', con, if_exists='append', index=True)

    if is_contacts_info:
        contacts.to_sql('contacts', con, if_exists='append', index=True)
    if is_locations_info:
        locations.to_sql('locations', con, if_exists='append', index=True)

    con.close()


def to_csv(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a comma-separated values (CSV) file.

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save a pandas DataFrame as a comma-separated values (CSV) file using a
        comma (',') to separate values.
    """
    filename = output + '.csv'
    filepath = path.joinpath(filename)

    df.to_csv(filepath, index=False, quoting=csv.QUOTE_NONNUMERIC)


def to_excel(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a Microsoft Excel Spreadsheet (XLSX file).

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save a pandas DataFrame as a Microsoft Excel spreadsheet using XLSX file
        format (Microsoft Excel 2007 and later).
    """
    filename = output + '.xlsx'
    filepath = path.joinpath(filename)

    df.to_excel(filepath, index=False)

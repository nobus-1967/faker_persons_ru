"""Module for generating output files (CSV, Common SQL, SQLite, MS Excel)."""
import csv
import sqlite3
import pandas as pd

from pathlib import Path


BEGIN = 'BEGIN TRANSACTION;\n'
COMMIT = '\nCOMMIT;'
SQL_CREATE_PERSONS_TABLE = """
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
SQL_CREATE_CONTACTS_TABLE = """
    CREATE TABLE IF NOT EXISTS contacts
    (
    ID INTEGER NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
"""
SQL_CREATE_LOCATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS locations
    (
    ID INTEGER NOT NULL,
    region TEXT NOT NULL,
    locality TEXT,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
"""
SQL_INSERT_PERSON_VALUE = """
INSERT INTO persons VALUES({},'{}','{}','{}','{}','{}');
"""
SQL_INSERT_CONTACT_VALUE = """
INSERT INTO contacts VALUES({},'{}','{}');
"""
SQL_INSERT_LOCATIONS_VALUE = """
INSERT INTO locations VALUES({},'{}','{}');
"""
SQL_PERSONS_COLUMNS = [
    'lastname',
    'firstname',
    'patronymic',
    'sex',
    'date_of_birth',
]
SQL_CONTACTS_COLUMNS = ['phone', 'email']
SQL_LOCATIONS_COLUMNS = ['region', 'locality']


def generate_sql(
    df: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate Common SQL file (tables: 'persons', 'contacts', localities').

    Args:
        df: pandas DataFrame - fake persons and (if were chosen) their contacts.
        output: string - file name (without extension).
        path: PosixPath - user home directory.

    Notes:
        save DataFrames as common SQL file (may be imported into RDBMS).
        use generic data types (TEXT for strings, DATE for dates).
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
        outfile.write(BEGIN)
        outfile.write(SQL_CREATE_PERSONS_TABLE)

        if is_contacts_info:
            outfile.write(SQL_CREATE_CONTACTS_TABLE)
        if is_contacts_info:
            outfile.write(SQL_CREATE_LOCATIONS_TABLE)

        for row in persons.itertuples():
            ID, lastname, firstname, patronymic, sex, date_of_birth = row
            outfile.write(
                SQL_INSERT_PERSON_VALUE.format(
                    ID, lastname, firstname, patronymic, sex, date_of_birth
                )
            )
        if is_contacts_info:
            for row in contacts.itertuples():
                ID, phone, email = row
                outfile.write(
                    SQL_INSERT_CONTACT_VALUE.format(ID, phone, email)
                )
        if is_locations_info:
            for row in locations.itertuples():
                ID, region, locality = row
                outfile.write(
                    SQL_INSERT_LOCATIONS_VALUE.format(ID, region, locality)
                )

        outfile.write(COMMIT)


def generate_sqlite3(
    df: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate SQLite3 file (tables: 'persons', 'contacts', 'localities').

    Args:
        df: pandas DataFrame - fake persons and (if were chosen) their contacts.
        output: string - file name (without extension).
        path: PosixPath - user home directory.

    Notes:
        save DataFrames as SQLite3 database file.
        use generic data types (TEXT for strings, DATE for dates).
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


def generate_csv(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate comma-separated values (CSV) file.

    Args:
        df: pandas DataFrame - fake persons and (if were chosen) their contacts.
        output: string - file name (without extension).
        path: PosixPath - user home directory.

    Notes:
        save DataFrames as comma-separated values (CSV) file.
        uses a comma (',') to separate values.
    """
    filename = output + '.csv'
    filepath = path.joinpath(filename)

    df.to_csv(filepath, index=False, quoting=csv.QUOTE_NONNUMERIC)


def generate_excel(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate Microsoft Excel Spreadsheet (XLSX file).

    Args:
        f: pandas DataFrame - fake persons and (if were chosen) their contacts.
        output: string - file name (without extension).
        path: PosixPath - user home directory.

    Notes:
        save DataFrames as Microsoft Excel spreadsheet.
        uses XLSX file format (Microsoft Excel 2007 and later).
    """
    filename = output + '.xlsx'
    filepath = path.joinpath(filename)

    df.to_excel(filepath, index=False)

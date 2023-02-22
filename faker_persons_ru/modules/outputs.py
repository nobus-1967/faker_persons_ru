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
SQL_INSERT_PERSON_VALUE = """
INSERT INTO persons VALUES({},'{}','{}','{}','{}','{}');
"""
SQL_INSERT_CONTACT_VALUE = """
INSERT INTO contacts VALUES({},'{}','{}');
"""
SQL_PERSONS_COLUMNS = [
    'lastname',
    'firstname',
    'patronymic',
    'sex',
    'date_of_birth',
]
SQL_CONTACTS_COLUMNS = ['phone', 'email']


def generate_sql(
    df_persons: pd.DataFrame,
    df_contacts: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate Common SQL file (tables: 'persons', 'contacts').

    Args:
        df_persons: pandas DataFrame with fake persons (name, sex,
        date of birth).
        df_contacts: pandas DataFrame with fake contacts (phones, emails).
        output: string for file name (without extension).
        path: PosixPath for home directory of user.

    Notes:
        use generic data types (TEXT for strings, DATE for dates).
    """
    filename = output + '.sql'
    filepath = path.joinpath(filename)

    with open(filepath, 'w') as outfile:
        outfile.write(BEGIN)
        outfile.write(SQL_CREATE_PERSONS_TABLE)
        outfile.write(SQL_CREATE_CONTACTS_TABLE)

        for row in df_persons.itertuples():
            ID, lastname, firstname, patronymic, sex, date_of_birth = row
            outfile.write(
                SQL_INSERT_PERSON_VALUE.format(
                    ID, lastname, firstname, patronymic, sex, date_of_birth
                )
            )

        for row in df_contacts.itertuples():
            ID, phone, email = row
            outfile.write(SQL_INSERT_CONTACT_VALUE.format(ID, phone, email))

        outfile.write(COMMIT)


def generate_sqlite3(
    df_persons: pd.DataFrame,
    df_contacts: pd.DataFrame,
    output: str,
    path: Path,
) -> None:
    """Generate SQLite3 file (tables: 'persons', 'contacts').

    Args:
        df_persons: pandas DataFrame with fake persons (name, sex,
        date of birth).
        df_contacts: pandas DataFrame with fake contacts (phones, emails).
        output: string for file name (without extension).
        path: PosixPath for home directory of user.

    Notes:
        use generic data types (TEXT for strings, DATE for dates).
    """
    filename = output + '.sqlite3'
    filepath = path.joinpath(filename)
    if filepath.is_file():
        filepath.unlink()

    dict_replace_persons = {
        x: y for (x, y) in zip(df_persons.columns, SQL_PERSONS_COLUMNS)
    }
    persons = df_persons.rename(columns=dict_replace_persons)

    dict_replace_contacts = {
        x: y for (x, y) in zip(df_contacts.columns, SQL_CONTACTS_COLUMNS)
    }
    contacts = df_contacts.rename(columns=dict_replace_contacts)

    con = sqlite3.connect(filepath)
    cur = con.cursor()

    cur.execute(SQL_CREATE_PERSONS_TABLE)
    cur.execute(SQL_CREATE_CONTACTS_TABLE)

    persons.to_sql('persons', con, if_exists='append', index=True)
    contacts.to_sql('contacts', con, if_exists='append', index=True)

    con.close()


def generate_csv(df_full: pd.DataFrame, output: str, path: Path) -> None:
    """Generate comma-separated values (CSV) file.

    Args:
        df_full: pandas DataFrame with fake persons & their contacts (name,
        sex, date of birth, phones, emails).
        output: string for file name (without extension).
        path: PosixPath for home directory of user.

    Notes:
        uses a comma (',') to separate values.
    """
    filename = output + '.csv'
    filepath = path.joinpath(filename)

    df_full.to_csv(filepath, index=False, quoting=csv.QUOTE_NONNUMERIC)


def generate_excel(df_full: pd.DataFrame, output: str, path: Path) -> None:
    """Generate Microsoft Excel Spreadsheet (XLSX file).

    Args:
        df_full: pandas DataFrame with fake persons & their contacts (name,
        sex, date of birth, phones, emails).
        output: string for file name (without extension).
        path: PosixPath for home directory of user.

    Notes:
        uses XLSX file format (Microsoft Excel 2007 and later).
    """
    filename = output + '.xlsx'
    filepath = path.joinpath(filename)

    df_full.to_excel(filepath, index=False)

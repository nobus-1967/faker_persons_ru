"""Module for generating output files (CSV, MS Excel, SQL, SQLite, MySQL)."""
import csv
import sqlite3
import sys
import pandas as pd

from pathlib import Path

SQL_PERSONS_COLUMNS: list[str] = [
    'lastname',
    'firstname',
    'patronymic',
    'sex',
    'date_of_birth',
]
SQL_CONTACTS_COLUMNS: list[str] = ['phone', 'email']
SQL_LOCATIONS_COLUMNS: list[str] = ['region', 'locality']
STDOUT = sys.stdout


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


def to_sql(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a common SQL file.

    Tables: 'persons', 'contacts' and 'locations'.

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save pandas DataFrames as a common SQL file (may be imported into RDBMS)
        using generic data types (INTEGER for integers, TEXT for strings, DATE
        for dates).
    """
    filename = output + '.sql'
    filepath = path.joinpath(filename)

    sql_create_persons_table: str = """
    CREATE TABLE IF NOT EXISTS `persons`
    (
    `ID` INTEGER NOT NULL PRIMARY KEY,
    `lastname` TEXT NOT NULL,
    `firstname` TEXT NOT NULL,
    `patronymic` TEXT NOT NULL,
    `sex` TEXT NOT NULL,
    `date_of_birth` DATE NOT NULL
    );
    """
    sql_create_contacts_table: str = """
    CREATE TABLE IF NOT EXISTS `contacts`
    (
    `ID` INTEGER NOT NULL,
    `phone` TEXT NOT NULL,
    `email` TEXT NOT NULL,
    FOREIGN KEY (`ID`) REFERENCES persons (`ID`) ON DELETE CASCADE
    );
    """
    sql_create_locations_table: str = """
    CREATE TABLE IF NOT EXISTS `locations`
    (
    `ID` INTEGER NOT NULL,
    `region` TEXT NOT NULL,
    `locality` TEXT NOT NULL,
    FOREIGN KEY (`ID`) REFERENCES persons (`ID`) ON DELETE CASCADE
    );
    """

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
            '-- You have to create database manually and run this file!\n\n'
        )
        outfile.write('BEGIN TRANSACTION;\n')

        outfile.write('\n-- Create table `persons`:\n')
        outfile.write(sql_create_persons_table)

        if is_contacts_info:
            outfile.write('\n-- Create table `contacts`:\n')
            outfile.write(sql_create_contacts_table)
        if is_contacts_info:
            outfile.write('\n-- Create table `contacts`:\n')
            outfile.write(sql_create_locations_table)

        outfile.write('\n-- Dump data for table `persons`:\n')

        for row in persons.itertuples():
            ID, lastname, firstname, patronymic, sex, date_of_birth = row
            outfile.write(
                'INSERT INTO `persons` VALUES '
                + f'({ID}, "{lastname}", "{firstname}", "{patronymic}", '
                + f'"{sex}", "{date_of_birth}");\n'
            )

        if is_contacts_info:
            outfile.write('\n-- Dump data for table `contacts`:\n')

            for row in contacts.itertuples():
                ID, phone, email = row
                outfile.write(
                    'INSERT INTO `contacts` VALUES '
                    + f'({ID}, "{phone}", "{email}");\n'
                )

        if is_locations_info:
            outfile.write('\n-- Dump data for table `locations`:\n')

            for row in locations.itertuples():
                ID, region, locality = row
                outfile.write(
                    'INSERT INTO `locations` VALUES '
                    + f'({ID}, "{region}", "{locality}");\n'
                )

        outfile.write('\nCOMMIT;')


def to_sqlite3(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a SQLite3 file.

    Tables: 'persons', 'contacts' and 'locations'.

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save pandas DataFrames as a SQLIte3 database.
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

    sql_create_persons_table: str = """
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
    sql_create_contacts_table: str = """
    CREATE TABLE IF NOT EXISTS contacts
    (
    ID INTEGER NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
    """
    sql_create_locations_table: str = """
    CREATE TABLE IF NOT EXISTS locations
    (
    ID INTEGER NOT NULL,
    region TEXT NOT NULL,
    locality TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES persons (ID) ON DELETE CASCADE
    );
    """

    cur.execute(sql_create_persons_table)

    if is_contacts_info:
        cur.execute(sql_create_contacts_table)
    if is_locations_info:
        cur.execute(sql_create_locations_table)

    persons.to_sql('persons', con, if_exists='append', index=True)

    if is_contacts_info:
        contacts.to_sql('contacts', con, if_exists='append', index=True)
    if is_locations_info:
        locations.to_sql('locations', con, if_exists='append', index=True)

    con.close()


def to_mysql(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a SQL file for MySQL/MariaDB.

    Tables: 'persons', 'contacts' and 'locations'.

    Args:
        df: A dataset (pandas DataFrame) containing fake Russian
        personal data; each record may include full name, sex, date of birth,
        cell phone number and email address, region and populated locality.
        output: A file name without extension (str).
        path: A path (PosixPath) to user's home directory.

    Notes:
        Save pandas DataFrames as a SQL file to import into MySQL/MariaDB.
    """
    filename = output + '.mysql'
    filepath = path.joinpath(filename)

    sql_create_persons_table: str = """
    DROP TABLE IF EXISTS `persons`;
    CREATE TABLE `persons`
    (
    `ID` SMALLINT NOT NULL,
    `lastname` VARCHAR(20) NOT NULL,
    `firstname` VARCHAR(20) NOT NULL,
    `patronymic` VARCHAR(20) NOT NULL,
    `sex` CHAR(4) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    PRIMARY KEY (`ID`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """
    sql_create_contacts_table: str = """
    DROP TABLE IF EXISTS `contacts`;
    CREATE TABLE `contacts`
    (
    `ID` SMALLINT NOT NULL,
    `phone` CHAR(16) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    KEY `ID` (`ID`),
    CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `persons` (`ID`)
    ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """
    sql_create_locations_table: str = """
    DROP TABLE IF EXISTS `locations`;
    CREATE TABLE locations
    (
    `ID` SMALLINT NOT NULL,
    `region` VARCHAR(50) NOT NULL,
    `locality` VARCHAR(50) NOT NULL,
    KEY `ID` (`ID`),
    CONSTRAINT `locations_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `persons` (`ID`)
    ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """

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
        sys.stdout = outfile
        print('-- Run this file in MySQL/MariaDB!\n\n')
        print('CREATE DATABASE IF NOT EXISTS `faker_persons_ru`;\n')
        print('USE `faker_persons_ru`;\n')

        print('\n-- Create table `persons`:\n')
        print(sql_create_persons_table)

        print('\n-- Dump data for table `persons`:\n')
        print('\nLOCK TABLES `persons` WRITE;\n')
        print('INSERT INTO `persons` VALUES')

        persons_lst = []

        for row in persons.itertuples():
            ID, lastname, firstname, patronymic, sex, date_of_birth = row
            persons_lst.append(
                f'({ID}, "{lastname}", "{firstname}", "{patronymic}", '
                + f'"{sex}", "{date_of_birth}")'
            )

        print(*persons_lst, sep=',\n')
        print(';\nUNLOCK TABLES;\n')

        if is_contacts_info:
            print('\n-- Create table `contacts`:\n')
            print(sql_create_contacts_table)

            print('\n-- Dump data for table `contacts`:\n')
            print('\nLOCK TABLES `contacts` WRITE;\n')
            print('INSERT INTO `contacts` VALUES ')

            contacts_lst = []

            for row in contacts.itertuples():
                ID, phone, email = row
                contacts_lst.append(f'({ID}, "{phone}", "{email}")')

            print(*contacts_lst, sep=',\n')
            print(';\nUNLOCK TABLES;\n')

        if is_locations_info:
            print('\n-- Create table `locations`:\n')
            print(sql_create_locations_table)

            print('\n-- Dump data for table `locations`:\n')
            print('\nLOCK TABLES `locations` WRITE;\n')
            print('INSERT INTO `locations` VALUES ')

            locations_lst = []

            for row in locations.itertuples():
                ID, region, locality = row
                locations_lst.append(f'({ID}, "{region}", "{locality}")')

            print(*locations_lst, sep=',\n')
            print(';\nUNLOCK TABLES;\n')

        print('\n-- Dump completed.')
        sys.stdout = STDOUT

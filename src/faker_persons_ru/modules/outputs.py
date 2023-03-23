"""Module for generating output files (CSV, MS Excel, SQL, SQLite, MySQL)."""
import csv
import sqlite3
import sys
import pandas as pd

from pathlib import Path

SQL_PERSON_COLUMNS: list[str] = [
    'last_name',
    'first_name',
    'patronymic',
    'sex',
    'date_of_birth',
]
SQL_CONTACT_COLUMNS: list[str] = ['phone', 'email']
SQL_LOCATION_COLUMNS: list[str] = ['region', 'locality']
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


def to_sqlite3(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a SQLite3 file.

    Tables: 'person', 'contact' and 'location'.

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

    is_contact_info = 'Телефон' and 'E-mail' in df.columns
    is_location_info = 'Регион' and 'Населённый пункт' in df.columns

    if is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
        location = df[['Регион', 'Населённый пункт']]
    elif is_contact_info and not is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
    elif not is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        location = df[['Регион', 'Населённый пункт']]
    else:
        person = df

    dict_replace_person = {
        x: y for (x, y) in zip(person.columns, SQL_PERSON_COLUMNS)
    }
    person = person.rename(columns=dict_replace_person)

    if is_contact_info:
        dict_replace_contact = {
            x: y for (x, y) in zip(contact.columns, SQL_CONTACT_COLUMNS)
        }
        contact = contact.rename(columns=dict_replace_contact)
    if is_location_info:
        dict_replace_location = {
            x: y for (x, y) in zip(location.columns, SQL_LOCATION_COLUMNS)
        }
        location = location.rename(columns=dict_replace_location)

    con = sqlite3.connect(filepath)
    cur = con.cursor()

    sql_create_person_table: str = """
    CREATE TABLE IF NOT EXISTS person
    (
    ID INTEGER NOT NULL PRIMARY KEY,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    sex TEXT NOT NULL,
    date_of_birth DATE NOT NULL
    );
    """
    sql_create_contact_table: str = """
    CREATE TABLE IF NOT EXISTS contact
    (
    ID INTEGER NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES person (ID) ON DELETE CASCADE
    );
    """
    sql_create_location_table: str = """
    CREATE TABLE IF NOT EXISTS location
    (
    ID INTEGER NOT NULL,
    region TEXT NOT NULL,
    locality TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES person (ID) ON DELETE CASCADE
    );
    """

    cur.execute(sql_create_person_table)

    if is_contact_info:
        cur.execute(sql_create_contact_table)
    if is_location_info:
        cur.execute(sql_create_location_table)

    person.to_sql('person', con, if_exists='append', index=True)

    if is_contact_info:
        contact.to_sql('contact', con, if_exists='append', index=True)
    if is_location_info:
        location.to_sql('location', con, if_exists='append', index=True)

    con.close()


def to_sql(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a common SQL file.

    Tables: 'person', 'contact' and 'location'.

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

    sql_create_person_table: str = """
    CREATE TABLE IF NOT EXISTS `person`
    (
    `ID` INTEGER NOT NULL PRIMARY KEY,
    `last_name` TEXT NOT NULL,
    `first_name` TEXT NOT NULL,
    `patronymic` TEXT NOT NULL,
    `sex` TEXT NOT NULL,
    `date_of_birth` DATE NOT NULL
    );
    """
    sql_create_contact_table: str = """
    CREATE TABLE IF NOT EXISTS `contact`
    (
    `ID` INTEGER NOT NULL,
    `phone` TEXT NOT NULL,
    `email` TEXT NOT NULL,
    FOREIGN KEY (`ID`) REFERENCES person (`ID`) ON DELETE CASCADE
    );
    """
    sql_create_location_table: str = """
    CREATE TABLE IF NOT EXISTS `location`
    (
    `ID` INTEGER NOT NULL,
    `region` TEXT NOT NULL,
    `locality` TEXT NOT NULL,
    FOREIGN KEY (`ID`) REFERENCES person (`ID`) ON DELETE CASCADE
    );
    """

    is_contact_info = 'Телефон' and 'E-mail' in df.columns
    is_location_info = 'Регион' and 'Населённый пункт' in df.columns

    if is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
        location = df[['Регион', 'Населённый пункт']]
    elif is_contact_info and not is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
    elif not is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        location = df[['Регион', 'Населённый пункт']]
    else:
        person = df

    with open(filepath, 'w') as outfile:
        sys.stdout = outfile
        print('-- You have to create database manually and run this file!\n\n')
        print('BEGIN TRANSACTION;\n')

        print('\n-- Create table `person`:\n')
        print(sql_create_person_table)

        if is_contact_info:
            print('\n-- Create table `contact`:\n')
            print(sql_create_contact_table)
        if is_contact_info:
            print('\n-- Create table `contact`:\n')
            print(sql_create_location_table)

        print('\n-- Dump data for table `person`:\n')

        person_lst = []

        for row in person.itertuples():
            ID, last_name, first_name, patronymic, sex, date_of_birth = row
            person_lst.append(
                'INSERT INTO `person` VALUES '
                + f'({ID}, "{last_name}", "{first_name}", "{patronymic}", '
                + f'"{sex}", "{date_of_birth}")'
            )

        print(*person_lst, sep=';\n', end=';\n')

        if is_contact_info:
            print('\n-- Dump data for table `contact`:\n')

            contact_lst = []

            for row in contact.itertuples():
                ID, phone, email = row
                contact_lst.append(
                    'INSERT INTO `contact` VALUES '
                    + f'({ID}, "{phone}", "{email}")'
                )

            print(*contact_lst, sep=';\n', end=';\n')

        if is_location_info:
            print('\n-- Dump data for table `location`:\n')

            location_lst = []

            for row in location.itertuples():
                ID, region, locality = row
                location_lst.append(
                    'INSERT INTO `location` VALUES '
                    + f'({ID}, "{region}", "{locality}")'
                )

            print(*location_lst, sep=';\n', end=';\n')

        print('\nCOMMIT;')
        sys.stdout = STDOUT


def to_mysql(df: pd.DataFrame, output: str, path: Path) -> None:
    """Generate a SQL file for MySQL/MariaDB.

    Tables: 'person', 'contact' and 'location'.

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

    sql_create_person_table: str = """
    DROP TABLE IF EXISTS `person`;
    CREATE TABLE `person`
    (
    `ID` SMALLINT NOT NULL,
    `last_name` VARCHAR(20) NOT NULL,
    `first_name` VARCHAR(20) NOT NULL,
    `patronymic` VARCHAR(20) NOT NULL,
    `sex` CHAR(4) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    PRIMARY KEY (`ID`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """
    sql_create_contact_table: str = """
    DROP TABLE IF EXISTS `contact`;
    CREATE TABLE `contact`
    (
    `ID` SMALLINT NOT NULL,
    `phone` CHAR(16) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    KEY `ID` (`ID`),
    CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `person` (`ID`)
    ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """
    sql_create_location_table: str = """
    DROP TABLE IF EXISTS `location`;
    CREATE TABLE `location`
    (
    `ID` SMALLINT NOT NULL,
    `region` VARCHAR(50) NOT NULL,
    `locality` VARCHAR(50) NOT NULL,
    KEY `ID` (`ID`),
    CONSTRAINT `location_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `person` (`ID`)
    ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """

    is_contact_info = 'Телефон' and 'E-mail' in df.columns
    is_location_info = 'Регион' and 'Населённый пункт' in df.columns

    if is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
        location = df[['Регион', 'Населённый пункт']]
    elif is_contact_info and not is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        contact = df[['Телефон', 'E-mail']]
    elif not is_contact_info and is_location_info:
        person = df[['Фамилия', 'Имя', 'Отчество', 'Пол', 'Дата рождения']]
        location = df[['Регион', 'Населённый пункт']]
    else:
        person = df

    with open(filepath, 'w') as outfile:
        sys.stdout = outfile
        print('-- Run this file in MySQL/MariaDB!\n\n')
        print('CREATE DATABASE IF NOT EXISTS `faker_persons_ru`;\n')
        print('USE `faker_persons_ru`;\n')

        print('\n-- Create table `person`:\n')
        print(sql_create_person_table)

        print('\n-- Dump data for table `person`:\n')
        print('\nLOCK TABLES `person` WRITE;\n')
        print('INSERT INTO `person` VALUES')

        person_lst = []

        for row in person.itertuples():
            ID, last_name, first_name, patronymic, sex, date_of_birth = row
            person_lst.append(
                f'({ID}, "{last_name}", "{first_name}", "{patronymic}", '
                + f'"{sex}", "{date_of_birth}")'
            )

        print(*person_lst, sep=',\n', end=';\n')
        print('\nUNLOCK TABLES;\n')

        if is_contact_info:
            print('\n-- Create table `contact`:\n')
            print(sql_create_contact_table)

            print('\n-- Dump data for table `contact`:\n')
            print('\nLOCK TABLES `contact` WRITE;\n')
            print('INSERT INTO `contact` VALUES ')

            contact_lst = []

            for row in contact.itertuples():
                ID, phone, email = row
                contact_lst.append(f'({ID}, "{phone}", "{email}")')

            print(*contact_lst, sep=',\n', end=';\n')
            print('\nUNLOCK TABLES;\n')

        if is_location_info:
            print('\n-- Create table `location`:\n')
            print(sql_create_location_table)

            print('\n-- Dump data for table `location`:\n')
            print('\nLOCK TABLES `location` WRITE;\n')
            print('INSERT INTO `location` VALUES ')

            location_lst = []

            for row in location.itertuples():
                ID, region, locality = row
                location_lst.append(f'({ID}, "{region}", "{locality}")')

            print(*location_lst, sep=',\n', end=';\n')
            print('\nUNLOCK TABLES;\n')

        print('\n-- Dump completed.')
        sys.stdout = STDOUT

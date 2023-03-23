"""Module for generating fake Russian emails based on fake Russian persons."""
import random

TRANSLIT: dict[str, str] = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'ie',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'iu',
    'я': 'ia',
    '_': '_',
    '-': '-',
    '.': '.',
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
}
PATTERNS: list[str] = [
    '{first_name}.{last_name}',
    '{first_name[0]}.{last_name}',
    '{last_name}.{first_name}',
    '{last_name}.{first_name[0]}',
    '{first_name}_{last_name}',
    '{first_name[0]}_{last_name}',
    '{last_name}_{first_name}',
    '{last_name}_{first_name[0]}',
    '{first_name}-{last_name}',
    '{first_name[0]}-{last_name}',
    '{last_name}-{first_name}',
    '{last_name}-{first_name[0]}',
    '{first_name[0]}{last_name}',
    '{first_name}.{last_name}.{year}',
    '{first_name[0]}.{last_name}.{year}',
    '{last_name}.{first_name}.{year}',
    '{last_name}.{first_name[0]}.{year}',
    '{first_name[0]}{last_name}.{year}',
    '{first_name[0]}{last_name}_{year}',
    '{first_name}_{last_name}_{year}',
    '{first_name[0]}_{last_name}_{year}',
    '{last_name}_{first_name}_{year}',
    '{last_name}_{first_name[0]}_{year}',
    '{first_name[0]}{last_name}-{year}',
    '{first_name}-{last_name}-{year}',
    '{first_name[0]}-{last_name}-{year}',
    '{last_name}-{first_name}-{year}',
    '{last_name}-{first_name[0]}-{year}',
    '{first_name}.{last_name}.{year[2]}{year[3]}',
    '{first_name[0]}.{last_name}.{year[2]}{year[3]}',
    '{last_name}.{first_name}.{year[2]}{year[3]}',
    '{last_name}.{first_name[0]}.{year[2]}{year[3]}',
    '{first_name[0]}{last_name}.{year[2]}{year[3]}',
    '{first_name[0]}{last_name}_{year[2]}{year[3]}',
    '{first_name}_{last_name}_{year[2]}{year[3]}',
    '{first_name[0]}_{last_name}_{year[2]}{year[3]}',
    '{last_name}_{first_name}_{year[2]}{year[3]}',
    '{last_name}_{first_name[0]}_{year[2]}{year[3]}',
    '{first_name[0]}{last_name}-{year[2]}{year[3]}',
    '{first_name}-{last_name}-{year[2]}{year[3]}',
    '{first_name[0]}-{last_name}-{year[2]}{year[3]}',
    '{last_name}-{first_name}-{year[2]}{year[3]}',
    '{last_name}-{first_name[0]}-{year[2]}{year[3]}',
]
DOMAINS: list[str] = [
    '@ruspost.online',
    '@ruspost.net',
    '@ruspost.net.ru',
    '@ruspost.ru.net',
    '@ruspost.su',
    '@ru-email.online',
    '@ru-email.net',
    '@ru-email.net.ru',
    '@ru-email.ru.net',
    '@ru-email.su',
]


def gen_email(base_dset: list[list[str]]) -> list[str]:
    """Generate a dataset of fake Russian email addresses.

    Args:
        base_dset: A dataset (list of lists of str) containing fake Russian
        personal data, including names and date of birth.

    Returns:
        A list of strings containing fake Russian email addresses based on
        Russian names and--if necessary--years of birth.
    """
    email_lst: list[str] = []

    for i, row in enumerate(base_dset):
        last_name = row[0]
        first_name = row[1]
        year = row[4][:4]
        var = i % 12

        email = gen_login(last_name, first_name, year, var)

        while email in email_lst:
            var += 1
            email = gen_login(last_name, first_name, year, var)

        email_lst.append(email)

    return email_lst


def translit_login(login_ru: str) -> str:
    """Generate email login for fake Russian name.

    Args:
        login_ru: A login (string) based on Russian name and--if
        necessary--year of birth.

    Returns:
        A string as a transliterated login_ru for generating fake personal
        email address.
    """
    login_en = ''

    for ch in login_ru.lower():
        login_en += TRANSLIT[ch]

    return login_en


def gen_login(last_name: str, first_name: str, year: str, var: int) -> str:
    """Generate email address for fake person from name and date of birth.

    Args:
        last_name: A Russian last name (str).
        first_name: A Russian first name (str).
        year: A person's year of birth (str).
        var: A number (int) for a pattern of email address.

    Returns:
        A str containing a fake Russian personal email address.
    """
    pattern = PATTERNS[var]
    domain = random.choice(DOMAINS)
    login_ru = pattern.format(
        last_name=last_name, first_name=first_name, year=year
    )
    email = translit_login(login_ru) + domain

    return email

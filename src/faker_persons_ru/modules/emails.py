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
    '{firstname}.{lastname}',
    '{firstname[0]}.{lastname}',
    '{lastname}.{firstname}',
    '{lastname}.{firstname[0]}',
    '{firstname}_{lastname}',
    '{firstname[0]}_{lastname}',
    '{lastname}_{firstname}',
    '{lastname}_{firstname[0]}',
    '{firstname}-{lastname}',
    '{firstname[0]}-{lastname}',
    '{lastname}-{firstname}',
    '{lastname}-{firstname[0]}',
    '{firstname[0]}{lastname}',
    '{firstname}.{lastname}.{year}',
    '{firstname[0]}.{lastname}.{year}',
    '{lastname}.{firstname}.{year}',
    '{lastname}.{firstname[0]}.{year}',
    '{firstname[0]}{lastname}.{year}',
    '{firstname[0]}{lastname}_{year}',
    '{firstname}_{lastname}_{year}',
    '{firstname[0]}_{lastname}_{year}',
    '{lastname}_{firstname}_{year}',
    '{lastname}_{firstname[0]}_{year}',
    '{firstname[0]}{lastname}-{year}',
    '{firstname}-{lastname}-{year}',
    '{firstname[0]}-{lastname}-{year}',
    '{lastname}-{firstname}-{year}',
    '{lastname}-{firstname[0]}-{year}',
    '{firstname}.{lastname}.{year[2]}{year[3]}',
    '{firstname[0]}.{lastname}.{year[2]}{year[3]}',
    '{lastname}.{firstname}.{year[2]}{year[3]}',
    '{lastname}.{firstname[0]}.{year[2]}{year[3]}',
    '{firstname[0]}{lastname}.{year[2]}{year[3]}',
    '{firstname[0]}{lastname}_{year[2]}{year[3]}',
    '{firstname}_{lastname}_{year[2]}{year[3]}',
    '{firstname[0]}_{lastname}_{year[2]}{year[3]}',
    '{lastname}_{firstname}_{year[2]}{year[3]}',
    '{lastname}_{firstname[0]}_{year[2]}{year[3]}',
    '{firstname[0]}{lastname}-{year[2]}{year[3]}',
    '{firstname}-{lastname}-{year[2]}{year[3]}',
    '{firstname[0]}-{lastname}-{year[2]}{year[3]}',
    '{lastname}-{firstname}-{year[2]}{year[3]}',
    '{lastname}-{firstname[0]}-{year[2]}{year[3]}',
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


def gen_emails(base_dset: list[list[str]]) -> list[str]:
    """Generate a dataset of fake Russian email addresses.

    Args:
        base_dset: A dataset (list of lists of str) containing fake Russian
        personal data, including names and date of birth.

    Returns:
        A list of strings containing fake Russian email addresses based on
        Russian names and--if necessary--years of birth.
    """
    emails_lst: list[str] = []

    for i, row in enumerate(base_dset):
        lastname = row[0]
        firstname = row[1]
        year = row[4][:4]
        var = i % 12

        email = gen_login(lastname, firstname, year, var)

        while email in emails_lst:
            var += 1
            email = gen_login(lastname, firstname, year, var)

        emails_lst.append(email)

    return emails_lst


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


def gen_login(lastname: str, firstname: str, year: str, var: int) -> str:
    """Generate email address for fake person from name and date of birth.

    Args:
        lastname: A Russian last name (str).
        firstname: A Russian first name (str).
        year: A person's year of birth (str).
        var: A number (int) for a pattern of email address.

    Returns:
        A str containing a fake Russian personal email address.
    """
    pattern = PATTERNS[var]
    domain = random.choice(DOMAINS)
    login_ru = pattern.format(
        lastname=lastname, firstname=firstname, year=year
    )
    email = translit_login(login_ru) + domain

    return email

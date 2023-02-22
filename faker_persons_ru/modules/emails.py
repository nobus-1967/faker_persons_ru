"""Module for generating fake emails based on fake names."""
import random

TRANSLIT = {
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
PATTERNS = [
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
DOMAINS = [
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


def generate_emails(dataset_persons: list[list[str]]) -> list[str]:
    """Generate a dataset of fake emails.

    Args:
        dataset_persons: list of lists (containing strings) with fake personal info.

    Returns:
        list of fake emails.
    """
    emails = list()

    for i, row in enumerate(dataset_persons):
        lastname = row[0]
        firstname = row[1]
        year = row[4][:4]
        var = i % 12

        email = generate_login(lastname, firstname, year, var)

        while email in emails:
            var += 1
            email = generate_login(lastname, firstname, year, var)

        emails.append(email)

    return emails


def transliterate_login(ru_login: str) -> str:
    """Generate email login for fake name.

    Args:
        ru_login: string for login in Russian.

    Returns:
        en_login as transliterated string.
    """
    en_login = ''

    for ch in ru_login.lower():
        en_login += TRANSLIT[ch]

    return en_login


def generate_login(lastname: str, firstname: str, year: str, var: int) -> str:
    """Generate email address for fake person (from name and date of birth).

    Args:
        lastname: string of Russian last name.
        firstname: string of Russian first name.
        year: string of person's year of birth.
        var: integer for a pattern of email address.

    Returns:
        string as fake email address.
    """
    pattern = PATTERNS[var]
    domain = random.choice(DOMAINS)
    ru_login = pattern.format(
        lastname=lastname, firstname=firstname, year=year
    )
    email = transliterate_login(ru_login) + domain

    return email

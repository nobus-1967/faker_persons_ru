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


def gen_emails(persons_dset: list[list[str]]) -> list[str]:
    """Generate a dataset of fake Russian email addresses.

    Args:
        persons_dset: list of lists (of str) - A dataset of Fake Russian
        records with personal info.

    Returns:
        A list (of str) containings fake Russian email addresses.
    """
    emails_lst: list[str] = []

    for i, row in enumerate(persons_dset):
        lastname = row[0]
        firstname = row[1]
        year = row[4][:4]
        var = i % 12

        email = gen_login(lastname, firstname, year, var)

        while emails_lst.count(email) > 0:
            var += 1
            email = gen_login(lastname, firstname, year, var)

        emails_lst.append(email)

    return emails_lst


def translit_login(login_ru: str) -> str:
    """Generate a login for a fake Russian email address.

    Args:
        login_ru: str - A login from Russian personal info (Russian letters).

    Returns:
        A login (str) as transliterated spelling for a fake email address.
    """
    login_en = ''

    for ch in login_ru.lower():
        login_en += TRANSLIT[ch]

    return login_en


def gen_login(lastname: str, firstname: str, year: str, var: int) -> str:
    """Generate an email address for a fake person.

    Args:
        lastname: str - A Russian last name.
        firstname: str - A Russian first name.
        year: str - A person's year of birth (use if neсessary).
        var: int - A number of a pattern of email addresses.

    Returns:
        A str as fake Russian personal email address.
    """
    pattern = PATTERNS[var]
    domain = random.choice(DOMAINS)
    login_ru = pattern.format(
        lastname=lastname, firstname=firstname, year=year
    )
    email = translit_login(login_ru) + domain

    return email

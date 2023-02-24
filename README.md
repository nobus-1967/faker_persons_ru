# faker_persons_ru

`EN`: Python3 project to generate fake personal data (in Russian): name, sex, date of birth, phone, email.

`RU`: Проект на Python3 для генерации фейковых русскоязычных персональных данных: Ф.И.О., пол, дата рождения, телефон, email.

## Описание проекта

Проект не является заменой [faker](https://faker.readthedocs.io). Он призван генерировать ограниченный массив *правдоподобной*, *качественной* и *естественной* персональной информации: русскоязычные фамилию, имя, отчество, номер мобильного телефона и адрес электронной почты.

**Правдоподобность** означает, что генерируемая информация внешне не будет существенно отличаться от реальных данных (то есть имена, телефонные номера, адреса электронной почты будут внешне казаться данными реальных людей).

**Качественность** и **естественность** достигаются использованием следующих принципов при отборе исходных данных и разработке алгоритма генерации массива информации:

- выбран диапазон **возрастов** от 18/19 лет (т.е. рождённые после распада СССР) до 64-65 лет (пенсионный возраст), далее этот диапазон разделён на три возрастные категории в соответствии с тем, как происходили существенные изменения в русском имяслове: *старшая* (старше 50 лет), родившаяся в эпоху, когда происходил постепенный переход от раннесоветских к устоявшимся советским традициям именования детей в русскоязычных семьях; *средняя* (старше 33 лет), когда к устоявшимся именам стали добавляться новые, особенно под влиянием политики открытости в период &laquo;перестройки&raquo; М.С.&nbsp;Горбачёва; и *младшая*, где наблюдается слом советских традиций именования и, как следствие, наибольшая дисперсия в присвоенных детям именах;

- для **фамилий** был взят за основу список из более 500 общерусских фамилий *А.Ф.&nbsp;Журавлева* (Журавлев А.Ф. К статистике русских фамилий. I // Вопросы ономастики. 2005. № 2. С. 126-146), каждой фамилии был определен свой *вес* по отношению к самой распространённой фамилии `Иванов`, поэтому при генерации списка данные фамилии дублируются в соответствии с их весами (как в реальной жизни, где часто встречаются однофамильцы);

- для **имён** старшего и среднего поколения использовалась весовая статистика именования новорожденных детей, взятая из проекта [&laquo;Популярность имен в Москве и области в XX веке&raquo;](https://names.mercator.ru/), для каждой из этих двух возрастных категорий было отобрано по 50 наиболее распространённых мужских и женских русских имён на 1970 и 1990 годы соответственно; для младшей возрастной категории использована статистика 75 самых встречаемых мужских и женских русских имён среди абитуриентов МГУ и СПбГУ, поступавших в 2015 году по данным проекта [&laquo;Тысяча имён&raquo;](https://1000names.ru/moda_na_imena);

- соответственно, мужские и женские **отчества** были произведены от наиболее распространённых имён предшествующей возрастной группы (а для старшей группы &mdash; от мужских имён 1940 года рождения и их весов), при этом при написании отчеств выбирался единственный вариант (например, `Геннадьевич`, а не `Геннадиевич`);

- **даты рождения** генерируются с проверкой на уникальность так, чтобы в одном массиве данных могли быть люди с одинаковыми Ф.И.О., как в реальной жизни, но рождённые в разное время (для их идентификации);

- **номера мобильных телефонов** генерируются случайным образом от &laquo;красивого&raquo; номера `111-00-11` до &laquo;красивого&raquo; номера `999-00-99` включительно, при этом случайным же образом каждый номер получал *код* из числа резервных, т.е. не задействованных в данный момент российскими мобильными операторами (`907`, `935`, `943`, `944`, `945`, `946`, `947`, `948`, `972`, `973`, `974`, `975` и `976`); таким образом, каждый номер в пределах одного генерируемого массива данных также является уникальным;

- уникальность и естественность **адресов электронной почты** обеспечивается тем, что используется более 40 распространённых шаблонов формирования данных адресов на основе имени, фамилии и года рождения, а также 10 фейковых доменов, т.е. несколько `Ивановых Иванов Ивановичей`, к примеру, получат разные адреса email.

## Опции программы

Программа `faker_persons_ru` представляет собой CLI-приложение, которое запускается из терминала с несколькими ключами-параметрами:

| Ключ                | Значение                                                    | Описание                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--help`            |                                                             | Выдаёт справку по использованию программы с данными ключами.                                                                                                                                                                                                                                                                                                                        |
| `--total`, `-t`     | целое число от `1` до `10000`                               | Количество записей (фейковых персональных данных) в генерируемом массиве. По умолчанию программа генерирует массив из `1000` строк-записей.                                                                                                                                                                                                                                         |
| `--output`, `-o`    | строка                                                      | Имя файла/файлов c генерируемым массивом данных (без расширения); если  в имени используются пробелы, строка заключается в кавычки.  Если параметр не задан, по умолчанию используется имя файла `new_dataset`. *Файлы создаются программой в домашней папке пользователя*!                                                                                                         |
| `--filetype`, `-f` | строка, выбор из вариантов: `csv`, `sql`, `sqlite3`, `xslx` | Расширение (тип) генерируемого файла/файлов (`CSV`-файл, `SQL`-файл для импорта в различные реляционные СУБД, готовая база данных СУБД `SQLite3` и файл `Microsoft Excel` версии 2007 года и новее). Если параметр не задан, то часть массива сгенерированных данных отображается только на экране. *Параметр может быть указан несколько раз для создания файлов различных типов*! |

Уникальность генерируемых данных проверенна на массиве в `100000` записей, однако, для обеспечения приемлемого времени отклика программы (несколько секунд) в данной версии максимальное число записей ограничено `10000`.

## Примеры использования программы:

1. `main.py` &mdash; генерация и частичный вывод на экран массива из `1000` записей;

2. `main.py --total 100` &mdash; генерация и частичный вывод на экран `100` записей;

3. `main.py -total 5000 --output my_dataset --fyletype csv` &mdash; генерация и частичный вывод на экран `5000` записей с сохранением массива данных в файл `my_dataset.csv` в домашней папке пользователя;

4. `main.py -t 10_000 -o 'big dataset' -f csv -f sqlite3` &mdash; генерация и частичный вывод на экран `10000` записей с сохранением массива данных в файлы `big dataset.csv` и `big dataset.sqlite3` в домашней папке пользователя;

5. `main.py --help` &mdash; вывод на экран справочной информации.

## Общая информация

Requirements/Зависимости программы: `click`, `pandas`

Author/Автор программы: Anatoly Shcherbina/Анатолий Щербина

Email: [avshcherbina@gmail.com](mailto:avshcherbina@gmail.com)

Version/Версия программы: `0.3.0`

Changelog/Изменения: [CHANGES.md](CHANGES.md)

License/Лицензия: `MIT`

---

Проект предназначен для использования в учебных целях и при разработке и тестировании ПО, когда возникает необходимость в массиве русскоязычных персональных данных.

**Любые содействие и помощь автору программы приветствуются!**

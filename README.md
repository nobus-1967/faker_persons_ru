# faker_persons_ru

`EN`: Python3 project to generate fake personal data (in Russian): name, sex, date of birth, phone, email, location.

`RU`: Проект на Python3 для генерации фейковых русскоязычных персональных данных: Ф.И.О., пол, дата рождения, телефон, email, место жительства.

## Описание проекта

**Проект не является заменой** [faker](https://faker.readthedocs.io). Он призван генерировать ограниченный массив *правдоподобной*, *качественной* и *естественной* персональной информации и квази-информации: русскоязычные фамилию, имя, отчество, номер мобильного телефона и адрес электронной почты, место жительства (регион, населённый пункт).

**Правдоподобность** означает, что генерируемая информация внешне не будет существенно отличаться от реальных данных (то есть имена, телефонные номера, адреса электронной почты будут внешне казаться данными реальных людей; для места жительства выбраны реально существующие населённые пункты).

**Качественность** и **естественность** достигаются использованием следующих принципов при отборе исходных данных и разработке алгоритма генерации массива информации:

- выбран диапазон **возрастов** от 18/19 лет (т.е. рождённые после распада СССР) до 64-65 лет (пенсионный возраст), далее этот диапазон разделён на три возрастные категории в соответствии с тем, как происходили существенные изменения в русском именнике (активно использующейся части именослова, всей совокупности имён в языке): *старшая* (старше 50 лет), родившаяся в эпоху, когда происходил постепенный переход от раннесоветских к устоявшимся советским традициям именования детей в русскоязычных семьях; *средняя* (старше 33 лет), когда к устоявшимся именам стали добавляться новые, особенно под влиянием политики открытости в период &laquo;перестройки&raquo; М.С.&nbsp;Горбачёва; и *младшая*, где наблюдается слом советских традиций именования и, как следствие, наибольшая дисперсия в присвоенных детям именах;

- в соответствии со статистическими данными (Численность населения Российской Федерации по полу и возрасту на 1 января 2022 года (Статистический бюллетень). М.: Росстат, 2022)  определён **удельный вес** упомянутых категорий населения в общем массиве генерируемой информации, а также **распределение по полу** внутри каждой возрастной группы (так, например, на каждые 100 чел. в возрасте 18-64 лет  приходится 31 чел. 1958-1972 годов рождения, среди которых женщины составляют 55%);

- для **фамилий** взят за основу список из более 500 общерусских фамилий *А.Ф.&nbsp;Журавлева* (Журавлев А.Ф. К статистике русских фамилий. I // Вопросы ономастики. 2005. № 2. С. 126-146), каждой фамилии был определен свой *вес* по отношению к самой распространённой фамилии `Иванов`, поэтому при генерации списка данные фамилии дублируются в соответствии с их весами (как в реальной жизни, где часто встречаются однофамильцы);

- для **имён** старшего и среднего поколения использовалась весовая статистика именования новорожденных детей, взятая из проекта [&laquo;Популярность имен в Москве и области в XX веке&raquo;](https://names.mercator.ru/), для каждой из этих двух возрастных категорий было отобрано по 50 наиболее распространённых мужских и женских русских имён на 1970 и 1990 годы соответственно; для младшей возрастной категории использована статистика 75 самых встречаемых мужских и женских русских имён среди абитуриентов МГУ и СПбГУ, поступавших в 2015 году по данным проекта [&laquo;Тысяча имён&raquo;](https://1000names.ru/moda_na_imena);

- соответственно, мужские и женские **отчества** произведены от наиболее распространённых имён предшествующей возрастной группы (а для старшей группы &mdash; от мужских имён 1940 года рождения и их весов), при этом при написании отчеств выбирался единственный вариант (например, `Геннадьевич`, а не `Геннадиевич`);

- **даты рождения** генерируются с проверкой на уникальность так, чтобы в одном массиве данных могли быть люди с одинаковыми Ф.И.О., как в реальной жизни, но рождённые в разное время (для их идентификации);

- **номера мобильных телефонов** генерируются случайным образом от &laquo;красивого&raquo; номера `111-00-11` до &laquo;красивого&raquo; номера `999-00-99` включительно, при этом случайным же образом каждый номер получает *код* из числа резервных &mdash; не задействованных в данный момент российскими мобильными операторами (`907`, `935`, `943`, `944`, `945`, `946`, `947`, `948`, `972`, `973`, `974`, `975` и `976`); таким образом, каждый номер в пределах одного генерируемого массива данных также является уникальным;

- уникальность и естественность **адресов электронной почты** обеспечивается тем, что используется более 40 распространённых шаблонов формирования данных адресов на основе имени, фамилии и года рождения, а также 10 фейковых доменов, т.е. несколько `Ивановых Иванов Ивановичей`, к примеру, получат разные адреса email;

- для генерации **места жительства** (регион России, населённый пункт) были отобраны свыше 1000 населённых пунктов с численностью жителей не менее 10000 чел. из различных краёв и областей по данным всероссийской переписи населения 2020 года ([Численность населения России, федеральных округов, субъектов Российской Федерации, городских округов, муниципальных районов, муниципальных округов, городских и сельских поселений, городских населенных пунктов, сельских населенных пунктов с населением 3000 человек и более](https://rosstat.gov.ru/storage/mediabank/tab-5_VPN-2020.xlsx)); в ряде случаев указан не только регион, но также городской/муниципальный округ (для населённых пунктов, входящих в данные округа, но не являющихся их административными центрами) и административный/муниципальный район (для населённых пунктов, не являющихся центрами данных районов); сокращённые наименования элементов места жительства (область, район, городской округ, посёлок и т.п.) приведены в соответствии с *Правилами сокращённого наименования адресообразующих элементов*, утверждёнными приказом Министерства финансов Российской Федерации от 05.11.2015 №&nbsp;171н.

Во всех случаях (имя, фамилия, наименование населённого пункта) там, где это предполагает произношение, употребляется русская буква `ё`.

## Опции программы

Программа `faker_persons_ru` представляет собой CLI-приложение, которое запускается из терминала с несколькими ключами-параметрами:

| Ключ               | Значение                                                            | Описание                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------ | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--help`           |                                                                     | Справка по использованию программы с данными ключами.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--total`, `-t`    | целое число от `1` до `100000`                                      | Количество записей (фейковых персональных данных) в генерируемом массиве. По умолчанию программа генерирует массив из `1000` строк-записей. *При вводе целого числа за пределами* `1-100000` *программа скорректирует его до ближайшего приемлемого значения.* **Если повторить ввод ключа с разными значениями несколько раз, то программа примет последнее заданное значение!**                                                                                                                                                                                 |
| `--data`, `-d`     | строка, выбор из вариантов: `base`, `contacts`, `locations`, `full` | Генерируемая программой фейковая информация: `base` (базовая &mdash; Ф.И.О., пол, дата рождения), `contacts` (базовая плюс контакты &mdash; номер телефона и адрес email), `locations` (базовая плюс место жительства &mdash; регион, населённый пункт) и `full` (полные данные &mdash; базовая информация, контакты и место жительства). *По умолчанию программа генерирует только базовую информацию, параметр* `base` *можно не указывать.* **Если повторить ввод ключа с разными значениями несколько раз, то программа примет последнее заданное значение!** |
| `--output`, `-o`   | строка                                                              | Имя файла/файлов c генерируемым массивом данных (без расширения); если  в имени используются пробелы, строка заключается в кавычки.  Если параметр не задан, по умолчанию используется имя файла `new_dataset`. *Файлы создаются программой в домашней папке пользователя.* **Если повторить ввод ключа с разными значениями несколько раз, то программа примет последнее заданное значение!**                                                                                                                                                                    |
| `--filetype`, `-f` | строка, выбор из вариантов: `csv`, `sql`, `sqlite3`, `xslx`         | Расширение (тип) генерируемого файла/файлов (`CSV`-файл, `SQL`-файл для импорта в различные реляционные СУБД, готовая база данных СУБД `SQLite3` и файл `Microsoft Excel` версии 2007 года и новее). *Если параметр не задан, то часть массива сгенерированных данных отображается только на экране.* **Параметр может быть указан несколько раз для создания файлов различных типов!**                                                                                                                                                                           |

Уникальность генерируемых данных проверена на массиве в `100000` записей, однако, для **обеспечения приемлемого времени отклика программы (несколько секунд) в данной версии рекомендуется ограничивать генерируемый массив** `10000` **уникальных записей**.

## Примеры использования программы:

1. `python[3] -m faker_persons_ru` &mdash; генерация и частичный вывод на экран массива из `1000` записей (базовая информация);

2. `python[3] -m faker_persons_ru --data base` — генерация и частичный вывод на экран массива из `1000` записей (базовая информация);

3. `python[3] -m faker_persons_ru --total 100 --data contacts` &mdash; генерация и частичный вывод на экран массива из `100` записей (базовая информация и контакты);

4. `python[3] -m faker_persons_ru --total 5000 --data locations --output my_dataset --fyletype csv` &mdash; генерация и частичный вывод на экран `5000` записей (базовая информация и место жительства) с сохранением массива данных в файл `my_dataset.csv` в домашней папке пользователя;

5. `python[3] -m faker_persons_ru -t 10_000 -d full -o 'big dataset' -f csv -f sqlite3` &mdash; генерация и частичный вывод на экран `10000` записей (полная информация) с сохранением массива данных в файлы `big dataset.csv` и `big dataset.sqlite3` в домашней папке пользователя;

6. `python[3] -m faker_persons_ru --help` &mdash; вывод на экран справочной информации.

## Установка:

1. Собрать и установить пакет из данного репозитория, например, в `GNU/Linux`:
- клонировать репозиторий на локальную рабочую станцию:

```bash
git clone https://github.com/nobus-1967/faker_persons_ru.git
cd faker_persons_ru/
```

- собрать пакет (собранный пакет появится в папке `faker_persons_ru/dist`):

```bash
python3 -m build
```

- далее установить пакет (лучше всего, как показано ниже &mdash; в *виртуальное окружение*, например, в виртуальную среду в папке `faker` в домашней директории пользователя):

```bash
python3.11 -m venv ~/faker
source ~/faker/bin/activate
pip install -U dist/*.whl
```

- запустить программу из виртуальной среды:

```bash
python -m faker_persons_ru
```

- и не забыть по окончании работы с программой выйти из виртуального окружения:

```bash
deactivate
```

2. Или скачать и установить готовый пакет последней версии: [Релизы](https://github.com/nobus-1967/faker_persons_ru/releases)

## Общая информация

Requirements/Зависимости программы: `click`, `pandas`

Author/Автор программы: Anatoly Shcherbina/Анатолий Щербина

Email: [avshcherbina@gmail.com](mailto:avshcherbina@gmail.com)

Changelog/Изменения: [CHANGES.md](CHANGES.md)

License/Лицензия: `MIT`

---

Проект предназначен для использования в учебных целях и при разработке и тестировании ПО, когда возникает необходимость в массиве русскоязычных персональных квази-данных.

**Любые содействие и помощь автору программы приветствуются!**

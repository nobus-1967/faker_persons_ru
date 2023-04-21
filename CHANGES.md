# CHANGES:

## 1.3.1 (2023-04-21)

- First final release, update 3.1: refactored datasets generation (using `tuple` with `dict`).

## 1.3.0 (2023-04-12)

- First final release, update 3.0: optimized datasets generation (using `dict`).

## 1.2.1 (2023-04-12)

- First final release, update 2.1: fixed typo in package's version.

## 1.2.0 (2023-03-23)

- First final release, update 2.0: refactored names of vars, modules and data tables (i.e. `lastname` to `last_name`, `outputs` to `output`, `persons` to `person`; plural was retained only for original dictionaries and lists of names/locations, `datasets` and `outputs` modules), fixed some typos.

## 1.1.2 (2023-03-20)

- First final release, update 1.2: unified dump for `SQL` and `MySQL/MariaDB` using `sys.stdout`.

## 1.1.1 (2023-03-19)

- First final release, update 1.1: fixed dump for `SQL`, `SQLite3` and `MySQL/MariaDB`.

## 1.1.0 (2023-03-12)

- First final release, update 1.0: fixed dump for `SQL` and `SQLite3`, added dump for `MySQL/MariaDB`.

## 1.0.0 (2023-03-12)

- First final release: refactored and cleaned code (mainly in `datasets` module), fixed docstrings.

## 0.9.0 (2023-03-10)

- Nineth pre-release (pre-final): refactored and cleaned code (birthday generations), fixed type hints, updated `README.md`.

## 0.8.0 (2023-03-10)

- Eighth pre-release: refactored and cleaned code (names of vars and functions, others), fixed dump for common `SQL` and `SQLite3`, improved docstrings.

## 0.7.2 (2023-03-08)

- Seventh pre-release: slightly simplified function `generate_persons` in module `dataset.py`.

## 0.7.1 (2023-03-07)

- Seventh pre-release: fixed dump for `SQL`.

## 0.7.0 (2023-03-05)

- Seventh pre-release: refactored `pandas` DataFrames generation.

## 0.6.2 (2023-03-05)

- Sixth pre-release: removed over-optimization, correct type hints, fixed `Click()` options and `README.md`.

## 0.6.1 (2023-03-04)

- Sixth pre-release: fixed `Click()` options.

## 0.6.0 (2023-03-04)

- Sixth pre-release: added data and code to generate information about location (place of residence).

## 0.5.1 (2023-03-04)

- Fifth pre-release: fixed import in `data/__init__.py`.

## 0.5.0 (2023-03-03)

- Fifth pre-release: added selection of generated information, renamed and refactored some modules, functions and variables.

## 0.4.1 (2023-02-26)

- Forth pre-release: partially refactored module `datasets`.

## 0.4.0 (2023-02-25)

- Forth pre-release: rewrited datasets generation algorithms.

## 0.3.1 (2023-02-24)

- Third pre-release: corrected vars.

## 0.3.0 (2023-02-24)

- Third pre-release: converted `csv` to dictionaries, corrected some last names, refactored module `names`, improved docstrings.

## 0.2.1 (2023-02-23)

- Second pe-release: added `__versions__.py`, improved docstrings.

## 0.2.0 (2023-02-23)

- Second pe-release: fixed import paths for modules, renamed data directory from 'sources' to 'data', improved docstrings.

## 0.1.0 (2023-02-22)

- Initial release.

# Бенчмарк "4 queries"
О бенчмарке: https://medium.unum.cloud/pandas-cudf-modin-arrow-spark-and-a-billion-taxirides-f85973bfafd5
Сырые данные: https://github.com/toddwschneider/nyc-taxi-data

## Установка
1. Склонировать проект
2. Установить Python 3.11.6: https://www.python.org/downloads/release/python-3116/
3. Установить "Разработка классических приложений на C++" с помощью Visual Studio Installer (для DuckDB): https://visualstudio.microsoft.com/ru/visual-cpp-build-tools/
4. Установить библиотеки из requirements.txt: pip install -r requirements.txt
5. Установить PostgreSQL 16.1: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

## Запуск
1. Скопировать в папку "data" csv-файл с данными
2. Изменить файл под нужный формат для работы с ними. Если данные взяты с https://drive.google.com/drive/folders/1usY-4CxLIz_8izBB9uAbg-JQEKSkPMg6:
2.1. Скомпилировать файл "data/fix.cpp" (подойдет почти любой компилятор для C++)
2.2. Запустить программу, передав в нее в качестве аргумента название csv-файла (без расширения)
3. Изменить файл "config.json":
3.1. "dataset": название csv-файла (без расширения)
3.2. "libraries": библиотеки для бенчмарка (можно указывать только те, что записаны изначально)
3.3. "queries": запросы для бенчмарка (от 1 до 4)
3.4. "postgres": параметры для входа в PostgreSQL
3.5. "tests": количество тестов
4. Запустить файл "main.py"

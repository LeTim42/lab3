# Бенчмарк "4 queries"
- [О бенчмарке](https://medium.unum.cloud/pandas-cudf-modin-arrow-spark-and-a-billion-taxirides-f85973bfafd5)
- [Сырые данные](https://github.com/toddwschneider/nyc-taxi-data)
- Использованные библиотеки: Psycopg2, SQLite, DuckDB, Pandas, SQLAlchemy

## Установка
1. Склонировать проект
2. Установить [Python 3.11.6](https://www.python.org/downloads/release/python-3116/)
3. Установить ***Разработка классических приложений на C++*** с помощью [Visual Studio Installer](https://visualstudio.microsoft.com/ru/visual-cpp-build-tools/) (для DuckDB)
4. Установить библиотеки из ***requirements.txt*** с помощью `pip install -r requirements.txt`
5. Установить [PostgreSQL 16.1](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

## Запуск
1. Скопировать в папку ***data*** csv-файл с данными
2. Изменить файл под нужный формат для работы с ними. Если данные взяты [отсюда](https://drive.google.com/drive/folders/1usY-4CxLIz_8izBB9uAbg-JQEKSkPMg6):
   - Скомпилировать файл ***fix.cpp*** (подойдет почти любой компилятор для C++)
   - Запустить программу, передав в нее в качестве аргумента название csv-файла (без расширения)
3. Изменить файл ***config.json***:
   - ***dataset***: название csv-файла (без расширения)
   - ***libraries***: библиотеки для бенчмарка (можно указывать только те, что записаны изначально)
   - ***queries***: запросы для бенчмарка (1, 2, 3, 4)
   - ***postgres***: параметры для входа в базу данных PostgreSQL
   - ***tests***: количество тестов
4. Запустить файл ***main.py***

## Выводы
По результатам бенчмарка на csv-файле размером 2 ГБ:
- Быстрее всех работает DuckDB: написана на C++, обрабатывает данные параллельно
- На втором месте Pandas: использует векторизацию, менее оптимизирована под SQL
- Psycopg2 и SQLAlchemy работают примерно одинаковое время: схожая реализация, оба загружают данные из PostgreSQL
- Медленнее всех работает SQLite: легкая библиотека, нет оптимизаций
Результаты и графики в ***results.xlsx***

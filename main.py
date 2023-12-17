from libraries import __psycopg2, __sqlite3, __duckdb, __pandas, __sqlalchemy
import json

libraries = {'psycopg2': __psycopg2.go,
             'sqlite3': __sqlite3.go,
             'duckdb': __duckdb.go,
             'pandas': __pandas.go,
             'sqlalchemy': __sqlalchemy.go}

try:
    with open('settings.json') as file:
        settings = json.load(file)
    for library in settings['libraries']:
        if libraries.get(library) is None:
            print(f"No such library '{library}'")
        else:
            print(f"Testing library '{library}'...")
            libraries[library](settings)
        print()
    input()
except Exception as e:
    print(e)
    input()
    exit(-1)

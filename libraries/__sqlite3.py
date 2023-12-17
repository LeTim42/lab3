from sqlite3 import connect
from csv import reader
import benchmark


def query(conn, cur, table, dataset, q):
    if q == 1:
        cur.execute(f"SELECT cab_type, count(*) FROM {dataset} GROUP BY 1;")
    elif q == 2:
        cur.execute(f"SELECT passenger_count, avg(total_amount) FROM {dataset} GROUP BY 1;")
    elif q == 3:
        cur.execute(f"SELECT passenger_count, strftime('%Y', 'pickup_datetime'), count(*) FROM {dataset} GROUP BY 1, 2;")
    elif q == 4:
        cur.execute(f"SELECT passenger_count, strftime('%Y', 'pickup_datetime'), round(trip_distance), count(*) FROM {dataset} GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;")


def go(settings):
    conn = connect('data/sqlite.db')
    cur = conn.cursor()
    dataset = settings['dataset']
    cur.execute(f"SELECT name FROM sqlite_schema WHERE type='table' AND name='{dataset}'")
    if not cur.fetchone():
        cur.execute(f"CREATE TABLE {dataset}(id BIGINT PRIMARY KEY,cab_type SMALLINT,pickup_datetime TIMESTAMP,dropoff_datetime TIMESTAMP,passenger_count FLOAT,trip_distance FLOAT,rate_code_id FLOAT,store_and_fwd_flag CHAR,pu_location_id SMALLINT,do_location_id SMALLINT,payment_type SMALLINT,fare_amount FLOAT,extra FLOAT,mta_tax FLOAT,tip_amount FLOAT,tolls_amount FLOAT,improvement_surcharge FLOAT,total_amount FLOAT,congestion_surcharge FLOAT,airport_fee FLOAT);")
        with open(f"data/{dataset}.csv", 'r') as file:
            file.readline()
            cur.executemany(f"INSERT INTO {dataset} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", reader(file))
            conn.commit()
    benchmark.go(settings, query, cur=cur)
    conn.close()

import psycopg2
import benchmark


def query(conn, cur, table, dataset, q):
    if q == 1:
        cur.execute(f"SELECT cab_type, count(*) FROM {dataset} GROUP BY 1;")
    elif q == 2:
        cur.execute(f"SELECT passenger_count, avg(total_amount) FROM {dataset} GROUP BY 1;")
    elif q == 3:
        cur.execute(f"SELECT passenger_count, extract(year from pickup_datetime), count(*) FROM {dataset} GROUP BY 1, 2;")
    elif q == 4:
        cur.execute(f"SELECT passenger_count, extract(year from pickup_datetime), round(trip_distance), count(*) FROM {dataset} GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;")


def go(settings):
    db_params = {}
    for setting in settings['postgres']:
        db_params[setting] = settings['postgres'][setting]
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    dataset = settings['dataset']
    cur.execute(f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{dataset}')")
    if not cur.fetchone()[0]:
        cur.execute(f"CREATE TABLE {dataset}(id BIGINT PRIMARY KEY,cab_type SMALLINT,pickup_datetime TIMESTAMP,dropoff_datetime TIMESTAMP,passenger_count FLOAT,trip_distance FLOAT,rate_code_id FLOAT,store_and_fwd_flag CHAR,pu_location_id SMALLINT,do_location_id SMALLINT,payment_type SMALLINT,fare_amount FLOAT,extra FLOAT,mta_tax FLOAT,tip_amount FLOAT,tolls_amount FLOAT,improvement_surcharge FLOAT,total_amount FLOAT,congestion_surcharge FLOAT,airport_fee FLOAT);")
        with open(f"data/{dataset}.csv", 'r') as file:
            file.readline()
            cur.copy_from(file, dataset, sep=',')
            conn.commit()
    benchmark.go(settings, query, cur=cur)
    conn.close()

from duckdb import connect
import benchmark


def query(conn, cur, table, dataset, q):
    if q == 1:
        conn.execute(f"SELECT cab_type, count(*) FROM {dataset} GROUP BY 1;")
    elif q == 2:
        conn.execute(f"SELECT passenger_count, avg(total_amount) FROM {dataset} GROUP BY 1;")
    elif q == 3:
        conn.execute(f"SELECT passenger_count, extract(year from pickup_datetime), count(*) FROM {dataset} GROUP BY 1, 2;")
    elif q == 4:
        conn.execute(f"SELECT passenger_count, extract(year from pickup_datetime), round(trip_distance), count(*) FROM {dataset} GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;")


def go(settings):
    conn = connect('data/duckdb.db')
    dataset = settings['dataset']
    conn.sql(f"CREATE TABLE IF NOT EXISTS {dataset} AS SELECT * FROM read_csv('data/{dataset}.csv', AUTO_DETECT=TRUE);")
    benchmark.go(settings, query, conn=conn)
    conn.close()

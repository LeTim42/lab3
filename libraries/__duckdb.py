from duckdb import connect
from time import time


def go(settings):
    conn = connect('duckdb.db')
    dataset = settings['dataset']
    conn.sql(f"CREATE TABLE IF NOT EXISTS {dataset} AS SELECT * FROM read_csv('data/{dataset}.csv', AUTO_DETECT=TRUE);")

    q = [f"SELECT cab_type, count(*) FROM {dataset} GROUP BY 1;",
         f"SELECT passenger_count, avg(total_amount) FROM {dataset} GROUP BY 1;",
         f"SELECT passenger_count, extract(year from pickup_datetime), count(*) FROM {dataset} GROUP BY 1, 2;",
         f"SELECT passenger_count, extract(year from pickup_datetime), round(trip_distance), count(*) FROM {dataset} GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;"]
    tests = int(settings['tests'])
    queries = settings['queries']
    times = [[0.0] * tests for _ in range(len(queries))]
    for j in range(tests):
        for i in range(len(queries)):
            start = time()
            res = conn.execute(q[int(queries[i])-1])
            # for r in res.fetchall(): print(r)
            finish = time()
            times[i][j] = finish - start
    for i in range(len(queries)):
        list.sort(times[i])
        print(f"Query {queries[i]}: {(times[i][tests//2+tests%2-1]+times[i][tests//2])/2:.3f} sec")
    conn.close()

from sqlalchemy import create_engine, orm, text
from time import time


def go(settings):
    engine = create_engine(f"postgresql://{settings['postgres']['user']}:{settings['postgres']['password']}@{settings['postgres']['host']}:{settings['postgres']['port']}/{settings['postgres']['dbname']}")
    cur = orm.sessionmaker(bind=engine)()
    dataset = settings['dataset']

    if not cur.execute(text(f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{dataset}')")).fetchone()[0]:
        cur.execute(text(f"CREATE TABLE {dataset}(id BIGINT PRIMARY KEY,cab_type SMALLINT,pickup_datetime TIMESTAMP,dropoff_datetime TIMESTAMP,passenger_count FLOAT,trip_distance FLOAT,rate_code_id FLOAT,store_and_fwd_flag CHAR,pu_location_id SMALLINT,do_location_id SMALLINT,payment_type SMALLINT,fare_amount FLOAT,extra FLOAT,mta_tax FLOAT,tip_amount FLOAT,tolls_amount FLOAT,improvement_surcharge FLOAT,total_amount FLOAT,congestion_surcharge FLOAT,airport_fee FLOAT);"))
        cur.commit()
        with open(f"data/{dataset}.csv", 'r') as file:
            file.readline()
            conn = engine.raw_connection()
            conn.cursor().copy_from(file, dataset, sep=',')
            conn.commit()

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
            res = cur.execute(text(q[int(queries[i])-1]))
            # for r in res.fetchall(): print(r)
            finish = time()
            times[i][j] = finish - start
    for i in range(len(queries)):
        list.sort(times[i])
        print(f"Query {queries[i]}: {(times[i][tests//2+tests%2-1]+times[i][tests//2])/2:.3f} sec")
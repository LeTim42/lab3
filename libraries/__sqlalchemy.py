from sqlalchemy import create_engine, orm, text
import benchmark


def query(conn, cur, table, dataset, q):
    if q == 1:
        cur.execute(text(f"SELECT cab_type, count(*) FROM {dataset} GROUP BY 1;"))
    elif q == 2:
        cur.execute(text("SELECT passenger_count, avg(total_amount) FROM {dataset} GROUP BY 1;"))
    elif q == 3:
        cur.execute(text("SELECT passenger_count, extract(year from pickup_datetime), count(*) FROM {dataset} GROUP BY 1, 2;"))
    elif q == 4:
        cur.execute(text("SELECT passenger_count, extract(year from pickup_datetime), round(trip_distance), count(*) FROM {dataset} GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;"))


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
    benchmark.go(settings, query, cur=cur)

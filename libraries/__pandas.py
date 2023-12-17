import pandas as pd
from os.path import exists
from time import time


def go(settings):
    pd.options.mode.chained_assignment = None
    dataset = settings['dataset']
    if not exists(f"data/{dataset}.pkl"):
        data = pd.read_csv(f"data/{dataset}.csv")
        data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
        data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime'])
        data.to_pickle(f"data/{dataset}.pkl")
    data = pd.read_pickle(f"data/{dataset}.pkl")

    tests = int(settings['tests'])
    queries = settings['queries']
    times = [[0.0] * tests for _ in range(len(queries))]
    for j in range(tests):
        for i in range(len(queries)):
            start = time()
            q = int(queries[i])
            if q == 1:
                selected_df = data[['cab_type']]
                grouped_df = selected_df.groupby('cab_type')
                final_df = grouped_df.size().reset_index(name='counts')
            elif q == 2:
                selected_df = data[['passenger_count', 'total_amount']]
                grouped_df = selected_df.groupby('passenger_count')
                final_df = grouped_df.mean().reset_index()
            elif q == 3:
                selected_df = data[['passenger_count', 'pickup_datetime']]
                selected_df['year'] = pd.to_datetime(
                    selected_df.pop('pickup_datetime'),
                    format='%Y-%m-%d %H:%M:%S').dt.year
                grouped_df = selected_df.groupby(['passenger_count', 'year'])
                final_df = grouped_df.size().reset_index(name='counts')
            elif q == 4:
                selected_df = data[[
                    'passenger_count',
                    'pickup_datetime',
                    'trip_distance']]
                selected_df['trip_distance'] = selected_df['trip_distance'].round().astype(int)
                selected_df['year'] = pd.to_datetime(
                    selected_df.pop('pickup_datetime'),
                    format='%Y-%m-%d %H:%M:%S').dt.year
                grouped_df = selected_df.groupby([
                    'passenger_count',
                    'year',
                    'trip_distance'])
                final_df = grouped_df.size().reset_index(name='counts')
                final_df = final_df.sort_values(
                    ['year', 'counts'],
                    ascending=[True, False])
            # print(final_df)
            finish = time()
            times[i][j] = finish - start
    for i in range(len(queries)):
        list.sort(times[i])
        print(f"Query {queries[i]}: {(times[i][tests // 2 + tests % 2 - 1] + times[i][tests // 2]) / 2:.3f} sec")

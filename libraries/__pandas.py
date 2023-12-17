import pandas as pd
from os.path import exists
import benchmark


def query(conn, cur, table, dataset, q):
    if q == 1:
        selected_df = table[['cab_type']]
        grouped_df = selected_df.groupby('cab_type')
        final_df = grouped_df.size().reset_index(name='counts')
    elif q == 2:
        selected_df = table[['passenger_count', 'total_amount']]
        grouped_df = selected_df.groupby('passenger_count')
        final_df = grouped_df.mean().reset_index()
    elif q == 3:
        selected_df = table[['passenger_count', 'pickup_datetime']]
        selected_df['year'] = pd.to_datetime(
            selected_df.pop('pickup_datetime'),
            format='%Y-%m-%d %H:%M:%S').dt.year
        grouped_df = selected_df.groupby(['passenger_count', 'year'])
        final_df = grouped_df.size().reset_index(name='counts')
    elif q == 4:
        selected_df = table[[
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


def go(settings):
    pd.options.mode.chained_assignment = None
    dataset = settings['dataset']
    if not exists(f"data/{dataset}.pkl"):
        table = pd.read_csv(f"data/{dataset}.csv")
        table['pickup_datetime'] = pd.to_datetime(table['pickup_datetime'])
        table['dropoff_datetime'] = pd.to_datetime(table['dropoff_datetime'])
        table.to_pickle(f"data/{dataset}.pkl")
    table = pd.read_pickle(f"data/{dataset}.pkl")
    benchmark.go(settings, query, table=table)

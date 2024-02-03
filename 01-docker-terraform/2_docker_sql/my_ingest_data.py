import pandas as pd
from time import time
from sqlalchemy import create_engine
import os
# ! new library
import argparse

# ! end of argparse bit
def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    file_name='output.csv.gz'
    csv_name='output.csv'
    # download the csv

    # ! fancy os.system use - use wget to get the url, output the csv name
    os.system(f"wget {url} -O {file_name}")
    os.system(f"gzip -d {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df = pd.read_csv(csv_name, nrows=100)
    
    # ! testing to see if this solves the issue of some columns defaulting to NULL in postgres
    df = df.convert_dtypes()

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

    df.head(0).to_sql(con=engine, name=table_name, if_exists='replace')
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000)
    df = next(df_iter) # uploading first 100k rows
    # ! testing to see if this solves the issue of some columns defaulting to NULL in postgres
    df = df.convert_dtypes()
    df.to_sql(con=engine, name=table_name, if_exists='replace')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            # ! testing to see if this solves the issue of some columns defaulting to NULL in postgres
            df = df.convert_dtypes()
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
            df.to_sql(con=engine, name=table_name, if_exists='append')
            t_end = time()
            print('inserted another chunk... Took %.3f seconds' % (t_end-t_start))
        except:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--table_name', help='destination table name')
    parser.add_argument('--url', help='url location of the file')
    
    args = parser.parse_args()

    main(args)

# ! command line entry will be:
# URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
# python my_ingest_data.py \
#     --user=root \
#     --password=root \
#     --host=localhost \
#     --port=5432 \
#     --db=ny_taxi \
#     --table_name=yellow_taxi_trips \
#     --url=${URL}
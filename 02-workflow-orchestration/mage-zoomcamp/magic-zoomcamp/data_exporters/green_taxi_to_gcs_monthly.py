import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/mage-keys.json"
bucket_name = 'mage-zoomcamp-marius'
project_id = 'cogent-weaver-411816'

table_name = 'green_taxi_data_monthly'
root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    data['lpep_pickup_month'] = data['lpep_pickup_datetime'].dt.month
    table = pa.Table.from_pandas(data)
    
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path = root_path,
        partition_cols = ['lpep_pickup_month'],
        filesystem = gcs
    )
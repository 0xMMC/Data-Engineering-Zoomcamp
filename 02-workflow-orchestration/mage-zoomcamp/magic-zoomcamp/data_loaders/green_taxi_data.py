import io
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    years = [2022]
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    dfs = []

    for year in years:
        for month in months:
            print(f'Reading {year}-{month}')
            base_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month}.parquet'
            df = pd.read_parquet(path=base_url)        
            dfs.append(df)
    
    dfs = pd.concat(dfs)

    return dfs


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

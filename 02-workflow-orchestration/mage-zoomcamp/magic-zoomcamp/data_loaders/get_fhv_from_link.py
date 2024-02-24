if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    years = [2019]
    months = ['02','03','04','05','06'] #,'07','08','09','10','11','12']
    dfs = []

    print('test')

    # for year in years:
    #     for month in months:
    #         print(f'Reading {year}-{month}')
    #         base_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month}.csv.gz'
    #         df = pd.read_csv(base_url)        
    #         dfs.append(df)
    
    year = 2019
    month = '12'
    base_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month}.csv.gz'
    df = pd.read_csv(base_url)

    # print(f"Combining {len(dfs)} dataframes.")
    # dfs = pd.concat(dfs)
    # print(f"Dataframes combined - {len(dfs)} total rows. Uploading ...")
    # return dfs

    return df


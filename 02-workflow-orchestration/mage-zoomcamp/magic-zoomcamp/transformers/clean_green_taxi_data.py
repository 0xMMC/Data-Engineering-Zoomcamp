import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Rows with zero passenger counts: { data['passenger_count'].isin([0]).sum() }")
    print(f"Rows with zero trip distance: { data['trip_distance'].isin([0]).sum() }")

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.strftime('%Y-%m-%d')

    data.columns = (data.columns
                    .str.replace(' ','_')
                    .str.lower()
    )

    print(data['vendorid'].value_counts())

    return data[(-data['passenger_count'].isin([0]))&(data['trip_distance']>0)]
    

@test
def test_output(output, *args) -> None:
    assert output['vendorid'] is not None, "Vendor ID is missing"
    assert output['passenger_count'].isin([0]).sum() == 0, "There are rides with zero passengers"
    assert output['trip_distance'].isin([0]).sum() == 0, "There are rides with zero trip distance"



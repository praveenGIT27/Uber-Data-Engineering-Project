import io
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loads Uber trip data from a public GCS bucket URL into a pandas DataFrame.
    Source: uber_data.csv (100,000 rows × 19 columns)
    """
    url = 'https://storage.googleapis.com/uber-data-praveen/uber_data.csv'
    response = requests.get(url)
    return pd.read_csv(io.StringIO(response.text), sep=',')


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'

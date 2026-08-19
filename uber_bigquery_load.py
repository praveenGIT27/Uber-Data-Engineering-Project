from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Exports all 8 dimension tables + fact table to BigQuery.
    Uses Application Default Credentials (VM service account).
    Config: io_config.yaml (default profile)
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    for key, value in data.items():
        df = DataFrame(value)
        table_id = f'project-16b0aeb7-f27f-4df7-b8f.uber_data.{key}'
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',
        )

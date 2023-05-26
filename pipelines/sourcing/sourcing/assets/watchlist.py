'''Software defined assets for source pipeline'''
# Python
import os

# 3rd party
import dagster as dg
import dotenv
import pandas as pd
import requests
# Project
from constants import TD_BASE_URL, INDICES
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv(), verbose=True)


@dg.asset
def top_pct_movers() -> dg.Output[pd.DataFrame]:
    """
    Fetches the top movers in a stock index from the
    TD Developer API and materializes it as an asset.

    Args:
        context (context): The context object provided by Dagster
        that contains information and utilities for the operation.
        index (str): The stock index for which to fetch the top movers.

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: If there is an error
        making the API request.

    Asset Materialization:
        The top movers data is saved as an asset with the stock index as
        the asset key. This allows the data to be tracked, stored, and
        used for lineage tracking and further analysis.

    Usage:
        fetch_top_movers("SPX")  # Fetches the top movers for the S&P 500
        and saves it as an asset.
    """
    comined_params = zip(INDICES, ['up', 'down'])
    logger = dg.get_dagster_logger()
    results = []
    for idx, direction in comined_params:
        endpoint = f"{TD_BASE_URL}{idx}/movers"
        params = {
            "apikey": os.environ['TD_KEY'],
            "direction": direction,
            "change": 'percent',
            "region": "us",
        }

        try:
            response = requests.get(endpoint, params=params, timeout=20)
            response.raise_for_status()
            movers = pd.DataFrame.from_dict(response.json())
            results.append(movers)
        except requests.exceptions.RequestException as exp:
            logger.error(
                f"Error fetching top movers for {(idx,direction)}: {str(exp)}"
            )
    results_df = pd.concat(results)
    # results_df.to_pickle(f'movers-{str(date.today())}.pkl')

    logger.info('Movers materialized!')

    return dg.Output(
        value=results_df,
        metadata={
            "num_records": len(results_df),
            "preview": dg.MetadataValue.md(
                results_df.head().to_markdown()
            ),
        },
    )

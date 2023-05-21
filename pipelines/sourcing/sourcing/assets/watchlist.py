'''Software defined assets for source pipeline'''
# Python
import os
from typing import List, Optional

# 3rd party
import dagster as dg
from dagster import Config
import dotenv
import pandas as pd
import requests

# Project
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv(), verbose=True)


class DataFetchConfig(Config):
    '''Dagster config for data fetch Ops'''
    index: str
    direction: str
    change: str


@dg.asset
def top_movers(
    context,
    config: DataFetchConfig,
) -> Optional[List]:
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
    endpoint = f"{os.environ['TD_BASE_URL']}{config.index}/movers"
    params = {
        "apikey": os.environ['TD_KEY'],
        "direction": config.direction,
        "change": config.change,
        "region": "us",
    }

    try:
        response = requests.get(endpoint, params=params, timeout=20)
        response.raise_for_status()
        movers = pd.DataFrame.from_dict(response.json())
        return dg.Output(value=movers)

    except requests.exceptions.RequestException as exp:
        context.log.error(
            f"Error fetching top movers for {config.index}: {str(exp)}"
        )

from dagster import job
from sourcing.assets.watchlist import top_pct_movers


@job
def fetch_top_pct_movers_job():
    '''Fetch top movers job'''
    # fetch_top_pct_movers()
    top_pct_movers()

from dagster import job

from sourcing.ops.watchlist import fetch_top_movers


@job
def fetch_top_movers_job(context):
    '''Fetch top movers job'''
    fetch_top_movers()

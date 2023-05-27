from dagster import job
# from dagster_slack import slack_on_success, SlackResource
# from sourcing.assets.watchlist import top_pct_movers
from sourcing.ops.watchlist import fetch_top_pct_movers


# @slack_on_success(
#     channel="#pipelines",
#     dagit_base_url="http://localhost:3000"
# )
@job()
def fetch_top_pct_movers_job():
    '''Fetch top movers job'''
    fetch_top_pct_movers()

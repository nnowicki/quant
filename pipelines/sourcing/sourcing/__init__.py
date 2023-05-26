'''Definitions for Dagster code locations'''
import os
import dagster as dg
from dagster_slack import SlackResource
# from sourcing.assets.watchlist import top_pct_movers
from sourcing.jobs import fetch_top_pct_movers_job
from sourcing.assets import watchlist
from sourcing.schedules import every_10_min

LOAD_PATH = "~/Desktop/projects/quant/pipelines/sourcing/"

defs = dg.Definitions(
    assets=dg.load_assets_from_modules([watchlist]),
    jobs=[fetch_top_pct_movers_job],
    # jobs=[
    #     dg.define_asset_job(
    #         'fetch_top_pct_movers_job',
    #         selection=dg.AssetSelection.all()
    #     )
    # ],
    schedules=[every_10_min],
    resources={
        "io_manager": dg.FilesystemIOManager(base_dir=LOAD_PATH),
        "slack": SlackResource(token=os.environ['SLACKBOT_KEY'])
    },
)

'''Definitions for Dagster code locations'''
import dagster as dg
from sourcing.assets.watchlist import top_movers
from jobs import fetch_top_movers_job
from schedules import every_weekday_9am

defs = dg.Definitions(
    assets=[top_movers],
    jobs=[fetch_top_movers_job],
    schedules=[every_weekday_9am],
)

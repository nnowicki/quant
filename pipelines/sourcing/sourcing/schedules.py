"""Collection of sourcing pipeline schedules"""

from dagster import schedule
from sourcing.jobs import fetch_top_pct_movers_job


@schedule(
    cron_schedule='*/5 * * * *',
    job=fetch_top_pct_movers_job,
    execution_timezone='US/Eastern',
)
def every_10_min(context):
    """Example of how to setup a weekday schedule for a job."""
    date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return {"ops": {"top_pct_movers": {"config": {"date": date}}}}

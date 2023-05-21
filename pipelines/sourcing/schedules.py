"""Collection of sourcing pipeline schedules"""

from dagster import schedule
from jobs import fetch_top_movers_job


@schedule(
    cron_schedule="0 9 * * 1-5",
    job=fetch_top_movers_job,
    execution_timezone="US/Eastern",
)
def every_weekday_9am(context):
    """Example of how to setup a weekday schedule for a job."""
    date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return {"ops": {"download_cereals": {"config": {"date": date}}}}

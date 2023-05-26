"""Example of how to run a Dagster op from normal Python script."""
from jobs import fetch_top_pct_movers_job

if __name__ == "__main__":
    result = fetch_top_pct_movers_job.execute_in_process()

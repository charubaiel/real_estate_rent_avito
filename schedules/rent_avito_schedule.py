
from dagster import schedule
from jobs.avito_dbd import parse_avito_data

@schedule(
    cron_schedule="15 */6 * * *",
    job=parse_avito_data,
    execution_timezone="Europe/Moscow",
)
def avito_schedule():
    return {}

from jobs.avito_dbd import parse_avito_data
from schedules.rent_avito_schedule import avito_schedule
from dagster import repository


@repository
def avito_dagster_parse():
    return [ parse_avito_data,
            avito_schedule,
            ]
from repositories.jobs.avito_dbd import parse_avito_agency_job,parse_avito_builders_job,parse_avito_users_job
from repositories.jobs.avito_dbd import avito_users_schedule,avito_agency_schedule,avito_builders_schedule
from repositories.jobs.ops.parse_avito_data import get_urls,fetch_pages
from dagster import repository



@repository
def avito_dagster_parse():

    jobs = [parse_avito_agency_job,
            parse_avito_builders_job,
            parse_avito_users_job]

    assets = [get_urls,fetch_pages]

    schedules = [avito_users_schedule,
                avito_agency_schedule,
                avito_builders_schedule]


    return [ 
            jobs,
            assets,
            schedules
            ]
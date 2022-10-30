from repositories.jobs.avito_dbd import parse_avito_job,avito_schedule
from repositories.jobs.ops.parse_avito_data import get_urls,update_db,fetch_pages
from dagster import repository



@repository
def avito_dagster_parse():
    return [ 
            parse_avito_job,
            avito_schedule,
            get_urls,update_db,fetch_pages
            ]
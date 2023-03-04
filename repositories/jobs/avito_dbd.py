
from dagster import define_asset_job,schedule

users_ads = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAkSSA8YQwMENuv03BkDKCCSEWYJZ5hYU5vwBkL4NFJauNay~DRSkxzWO3g4UApDeDhQC&p=1&s=104'
builders_ads = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAkSSA8YQwMENuv03BkDKCCSEWYJZ5hYU5vwBkL4NFJKuNay~DRSkxzWO3g4UApDeDhQC&p=1&s=104'
agency_ads = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAkSSA8YQwMENuv03BkDKCCSEWYJZ5hYU5vwBkL4NFJSuNay~DRSkxzWO3g4UApDeDhQC&p=1&s=104'

parse_avito_agency_job = define_asset_job(name='update_agency_avito',
                                    config={'ops': {"get_urls": {"config": {'url':agency_ads}},
                                                    "fetch_pages": {"config": {
                                                                                'n_pages': 10,
                                                                                'db_path':'data/RE_moscow_db.duckdb',
                                                                                'table_name':'agency_ads',
                                                                                }},
                                                    },
                                                    },
                                    tags={"dagster/max_retries": 1, "dagster/retry_strategy": "ALL_STEPS"})

parse_avito_users_job = define_asset_job(name='update_users_avito',
                                    config={'ops': {"get_urls": {"config": {'url':users_ads}},
                                                    "fetch_pages": {"config": {
                                                                                'n_pages': 6,
                                                                                'db_path':'data/RE_moscow_db.duckdb',
                                                                                'table_name':'user_ads',
                                                                                }},
                                                    },
                                                    },
                                    tags={"dagster/max_retries": 1, "dagster/retry_strategy": "ALL_STEPS"})

parse_avito_builders_job = define_asset_job(name='update_builders_avito',
                                    config={'ops': {"get_urls": {"config": {'url':builders_ads}},
                                                    "fetch_pages": {"config": {
                                                                                'n_pages': 14,
                                                                                'db_path':'data/RE_moscow_db.duckdb',
                                                                                'table_name':'builder_ads',
                                                                                }},
                                                    },
                                                    },
                                    tags={"dagster/max_retries": 1, "dagster/retry_strategy": "ALL_STEPS"})



@schedule(
    cron_schedule="39 19/20 * * *",
    job=parse_avito_agency_job,
    execution_timezone="Europe/Moscow",
)
def avito_users_schedule():
    return {}

@schedule(
    cron_schedule="57 */22 * * *",
    job=parse_avito_users_job,
    execution_timezone="Europe/Moscow",
)
def avito_builders_schedule():
    return {}

@schedule(
    cron_schedule="34 */18 * * *",
    job=parse_avito_builders_job,
    execution_timezone="Europe/Moscow",
)
def avito_agency_schedule():
    return {}




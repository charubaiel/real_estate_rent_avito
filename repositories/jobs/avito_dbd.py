
from dagster import define_asset_job,schedule


parse_avito_job = define_asset_job(name='update_avito',
                                    config={'ops': {"get_urls": {"config": {'url':'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAkSSA8YQwMENuv03A0DKCCSCWYRZjt4OFAKQ3g4UAg&i=1&p=1&s=104'}},
                                                    "fetch_pages": {"config": {"sleep_time": 5,
                                                                                'n_pages': 10}},
                                                    "update_db":{'config':{'db_path':'data/avito_db.duckdb'}},
                                                    },
                                                    },
                                    tags={"dagster/max_retries": 1, "dagster/retry_strategy": "ALL_STEPS"})



@schedule(
    cron_schedule="15 */6 * * *",
    job=parse_avito_job,
    execution_timezone="Europe/Moscow",
)
def avito_schedule():
    return {}
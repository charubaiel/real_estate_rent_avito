from ops.get_avito_start_data import *
from ops.parse_avito_data import fix_data, get_item_list
from dagster import job, get_dagster_logger as log, op, schedule,repository,config_from_files ,ScheduleDefinition
import sqlite3
import pandas as pd


@op
def save_to_sql(df_list):
    with sqlite3.connect('data/dagster_avito.db') as conn:
        for df in df_list:
            df.to_sql(con=conn, index=False,
                      name='moskva_re', if_exists='append')

        tables = pd.read_sql(
            "select name from sqlite_master where type='table' ", con=conn)
        for i in tables['name']:
            log().info('table {}  values: unique {} | ttl {}'
                       .format(i, *pd.read_sql(f"select count(distinct id) as uniq_ids,\
                                         count(id) as ttl_ids from {i} ", con=conn).values[0]))

@job(config=config_from_files(['ops.yaml']))
def get_result_df():

    save_to_sql(
        [fix_data(
            get_item_list(
                get_avito_page1()
            )
        ),
            fix_data(
            get_item_list(
                get_avito_page2()
            )
        ),
            fix_data(
            get_item_list(
                get_avito_page3()
            )
        ),
            fix_data(
            get_item_list(
                get_avito_page4()
            )
        ),
            fix_data(
            get_item_list(
                get_avito_page5()
            )
        )]
    )

# @schedule(
#     cron_schedule="16 8,18,23 * * *",
#     job=get_result_df,
#     execution_timezone="Europe/Moscow",
# )
# def avito_schedule(context):
#     date = context.scheduled_execution_time.strftime("%Y-%m-%d")
#     return {"ops": {"save_to_sql": {"config": {"date": date}}}}
basic_schedule = ScheduleDefinition(job=get_result_df, cron_schedule="28 10,18 * * *",execution_timezone="Europe/Moscow")
@repository
def avito_dagster_parse():
    return [ get_result_df, basic_schedule ]
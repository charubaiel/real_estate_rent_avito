from ops.get_avito_start_data import get_avito_page
from ops.parse_avito_data import fix_data, get_item_list, get_df_from_html
from dagster import job, get_dagster_logger as log, op
import sqlite3
import pandas as pd


@op
def save_to_sql(df):
    with sqlite3.connect('data/dagster_avito.db') as conn:
        df.to_sql(con=conn,index=False,table_name='moskva_re')
        df.log.info(f'Done! df_shape is {df.shape}')


@job
def get_result_df():

    save_to_sql(
        fix_data(
            get_df_from_html(
                get_item_list(
                    get_avito_page()
                    )
                )
        )
    )

    
    

    with sqlite3.connect('data/dagster_avito.db') as conn:
        tables = pd.read_sql("select name from sqlite_master where type='table' ",con = conn)
        for i in tables['name']:
            log().info('table {}  values: unique {} | ttl {}'\
                .format(i,*pd.read_sql(f"select count(distinct id) as uniq_ids,\
                                         count(id) as ttl_ids from {i} ",con = conn).values[0]))






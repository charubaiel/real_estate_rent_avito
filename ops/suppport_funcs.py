from dagster import op
import sqlite3
import pandas as pd

@op(description='get list of pages to parse')
def get_urls(context)->str:
    return context.op_config['url']


@op(description='save_result to local sql table')
def save_to_sql(context,df)-> None:
    params = context.op_config

    with sqlite3.connect(f'data/{params["db_name"]}') as conn:
        
        df.to_sql(con=conn, index=False,
                    name=params['table_name'], if_exists='append')

        tables = pd.read_sql(
            "select name from sqlite_master where type='table' ", con=conn)
        for i in tables['name']:
            context.log.info('table {}  values: unique {} | ttl {}'
                       .format(i, *pd.read_sql(f"select count(distinct id) as uniq_ids,\
                                         count(id) as ttl_ids from {i} ", con=conn).values[0]))


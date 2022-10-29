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
                    name=params['table_name'],
                    if_exists='append')

        tables = pd.read_sql(
            "select name from sqlite_master where type='table' ", con=conn)
        for i in tables['name']:
            context.log.info('table {}  values: unique {} | ttl {}'
                       .format(i, *pd.read_sql(f"select count(distinct id) as uniq_ids,\
                                         count(id) as ttl_ids from {i} ", con=conn).values[0]))

def get_item_info(item):
    item_desc = {}
    try:
        item_desc['datetime'] = pd.to_datetime('now')
        item_desc['publish_delta'] = item.find('div',{'data-marker':'item-date'}).text
        item_desc['id'] = item['id']
        item_desc['url'] = item.a['href']
        item_desc['title'] = item.a['title']
        item_desc['text'] = item.meta['content']
        item_desc['price'] = item.find('meta',{'itemprop':'price'})['content']
        try:
            item_desc['JK'] = item.find('div',{'data-marker':'item-development-name'})
        except:
            item_desc['JK'] = ''
        item_desc['adress'] = item.find('div',{'data-marker':'item-address'}).span.text
        item_desc['metro_dist'] = item.find('span',{'class':'geo-periodSection-bQIE4'}).text
        item_desc['metro'] = item.find('div',{'class':'geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL'}).text.replace(item_desc['metro_dist'],'')
        item_desc['metro_branch'] = item.find('i',{'class':'geo-icon-Cr9YM'})['style'].replace('background-color:','')
    except:
        pass

    return item_desc
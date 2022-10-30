import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from dagster import asset
from repositories.jobs.ops.support_funcs import (DatabaseConnection,
                                                 SeleniumConnection,
                                                 featuring_data, get_item_info)


@asset(description='get list of pages to parse')
def get_urls(context) -> str:
    return context.op_config['url']


@asset(description='collect raw html data',)
def fetch_pages(context, get_urls: str) -> list:

    parser = SeleniumConnection()
    pages = []

    for page in range(1, context.op_config['n_pages']+1):

        time.sleep(np.random.poisson(context.op_config['sleep_time']))
        get_urls = get_urls.replace('&p=1', f'&p={page}')
        response = parser.get(get_urls)
        if 'Продажа квартир в Москве' not in parser.parser.find_element('xpath', '//*[@id="app"]/div/div[3]/div[2]').text:
            break
        context.log.info(
            f'Parsed pages : {page}/{context.op_config["n_pages"]}')
        pages.append(response)

    parser.close_conn()
    return pages


@asset(description='extract structure data from html')
def update_db(context, fetch_pages: list) -> None:
    db = DatabaseConnection(context.op_config['db_path'])
    raw_data = []
    for html_data in fetch_pages:
        bs_data = BeautifulSoup(html_data, features='lxml')
        html_item_list = bs_data.find(
            'div', {'class': 'items-items-kAJAg'}).findAll('div', {'data-marker': 'item'})
        df_scheme = [get_item_info(i) for i in html_item_list]
        db.append_df(pd.DataFrame(df_scheme), schema='RAW')
        raw_data.extend(df_scheme)
    feature_rich_data = featuring_data(pd.DataFrame(df_scheme))
    db.append_df(feature_rich_data, schema='INTEL')
    db.close_conn()

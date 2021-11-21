import pandas as pd
import requests as r
import sqlite3
from bs4 import BeautifulSoup
import time
import numpy as np
from tqdm import tqdm
import logging
import argparse

#docker build -t rent_scan . | docker run --name scan_moscow -d -v rent_data_valut:/home/project/data:ro rent_scan



def get_item_list(html_data):
    bs = BeautifulSoup(html_data,features="lxml")
    return bs.find('div',{'class':'items-items-kAJAg'}).findAll('div',{'data-marker':'item'})

def get_item_info(item):
    item_desc = {}
    try:
        item_desc['date'] = pd.to_datetime('today').date()
        item_desc['publish_delta'] = item.find('div',{'data-marker':'item-date'}).text
        item_desc['id'] = item['id']
        item_desc['url'] = item.a['href']
        item_desc['title'] = item.a['title']
        item_desc['text'] = item.meta['content']
        item_desc['price'] = item.find('meta',{'itemprop':'price'})['content']
        item_desc['adress'] = item.find('div',{'data-marker':'item-address'}).span.text
        item_desc['metro'] = item.find('div',{'data-marker':'item-address'}).div.text.replace(item_desc['adress'],'').replace('\xa0',' ')
    except:
        pass

    return item_desc

def save_to_db(data,table_name,db_path):
    with sqlite3.connect(db_path) as w:
        pd.DataFrame(data).to_sql(name = table_name,con=w,if_exists='append')


def fix_data(data):
    df = data.copy()
    df['price'] = df['price'].astype(float)
    # df['home_num']=df['adress'].str.extract(', (\d.*)')
    df['street']=df['adress'].str.extract('(.*?), (?=\d.*)')
    df[['stantion','metro_distance']] = df['metro'].str.split(',',expand=True,n=1)
    df['metro_distance'] = df['metro_distance'].str.strip().str.split(' ',expand=True)[0].str.replace(',','.').astype(float).apply(lambda x: x*1000 if x<100 else x)
    df['n_rooms']=df['title'].str.extract('«(.*?),')
    df['m2'] = df['title'].str.extract(', (\d+).*м²').astype(float)
    df[['floor','max_floor']] = df['title'].str.extract('(\d+/\d+).*эт')[0].str.split('/',expand=True)
    df['text'] = df['text'].str.replace('\n','')
    df['rubm2'] = df['price'] / df['m2']
    df['rubm2m'] = df['rubm2'] * df['metro_distance'] / 1000
    df.drop(['title','adress','metro'],axis=1,inplace=True)
    return df
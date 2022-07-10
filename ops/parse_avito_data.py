from dagster import op
import pandas as pd
from utils import get_item_info
from bs4 import BeautifulSoup
import requests as r
import time
import numpy as np

FAKE_HISTORY = ['http://google.com',
                'http://hh.ru',
                'https://hh.ru/search/vacancy?area=&fromSearchLine=true&text=',
                'http://avito.ru',
                'https://www.avito.ru/moskva/nedvizhimost']

HEADERS={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}









@op(description='collect raw html data')
def get_pages(context,url:str)->list:
    pages = []

    with r.Session() as s:

        s.headers.update(HEADERS)
        [s.get(i) for i in FAKE_HISTORY];


        time.sleep(np.random.poisson(context.op_config['sleep_time']))
        
        response = s.get(url)

        if response.status_code != 200:
            
            raise ConnectionError(f'{response.status_code}\n{response.text}')

        max_pages = int(BeautifulSoup(response.text,'lxml').find('div',{'class':'pagination-root-Ntd_O'}).findAll('span',{'class':'pagination-item-JJq_j'})[-2].text)
        
        pages.append(response)
        
        for page in range(2,np.minimum(context.op_config['n_pages'],max_pages)):

            time.sleep(np.random.poisson(context.op_config['sleep_time']))

            url = url.replace('&p=1',f'&p={page}')
            response = s.get(url)

            if response.status_code != 200:
                
                raise ConnectionError(f'{response.status_code}\n{response.text}')
            context.log.info(f'Parsed pages : {page}/{max_pages}')    
            pages.append(response)

    return pages



@op(description='extract structure data from html')
def get_item_list(html_pages:list)-> pd.DataFrame: 
    data = pd.DataFrame()
    for html_data in html_pages:
        bs_data = BeautifulSoup(html_data.text,features='lxml')
        item_list = bs_data.find('div',{'class':'items-items-kAJAg'}).findAll('div',{'data-marker':'item'})
        df_scheme = [get_item_info(i) for i in item_list]
        data = data.append(pd.DataFrame(df_scheme))
    return data


@op(description='add features and humanize data')
def featuring_data(data:pd.DataFrame)->pd.DataFrame:
    df = data.copy()
    df['price'] = df['price'].astype(float)
    df['street']=df['adress'].str.extract('(.*?), (?=\d.*)')
    df['n_rooms']=df['title'].str.extract('«(.*?),')
    df['m2'] = df['title'].str.extract(', (\d+).*м²').astype(float)
    df[['floor','max_floor']] = df['title'].str.extract('(\d+/\d+).*эт')[0].str.split('/',expand=True).astype(float)
    df['text'] = df['text'].str.replace('\n','')
    df['rubm2'] = df['price'] / df['m2']
    df.drop(['title','adress'],axis=1,inplace=True)
    return df





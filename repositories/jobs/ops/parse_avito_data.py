from dagster import asset,graph
import pandas as pd
from repositories.jobs.ops.support_funcs import get_item_info
from bs4 import BeautifulSoup
import time
import numpy as np


HEADERS={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}




@asset(description='get list of pages to parse')
def get_urls(context)->str:
    return context.op_config['url']




@asset(description='collect raw html data')
def html_pages(context,get_urls:str)->list:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    firefox_options = Options()
    firefox_options.headless = True
    firefox_options.add_argument(f"HEADERS={HEADERS}")
    parser = webdriver.Firefox(options=firefox_options,executable_path='/home/charubaiel/.wdm/drivers/geckodriver/linux64/0.32/geckodriver')

    pages = []

    parser.get(get_urls)
    response = parser.find_element('xpath',"//*").get_attribute("outerHTML")


    max_pages = int(BeautifulSoup(response,'lxml').find('div',{'class':'pagination-root-Ntd_O'}).findAll('span',{'class':'pagination-item-JJq_j'})[-2].text)
    
    pages.append(response)
    
    for page in range(2,np.minimum(context.op_config['n_pages'],max_pages)):

        time.sleep(np.random.poisson(context.op_config['sleep_time']))

        get_urls = get_urls.replace('&p=1',f'&p={page}')
        try:
            parser.get(get_urls)
            response = parser.find_element('xpath',"//*").get_attribute("outerHTML")
        except:
            break

        context.log.info(f'Parsed pages : {page}/{max_pages}')    
        pages.append(response)

    parser.close()
    return pages



@asset(description='extract structure data from html')
def item_list(html_pages:list)-> pd.DataFrame: 
    data = pd.DataFrame()
    for html_data in html_pages:
        bs_data = BeautifulSoup(html_data,features='lxml')
        html_item_list = bs_data.find('div',{'class':'items-items-kAJAg'}).findAll('div',{'data-marker':'item'})
        df_scheme = [get_item_info(i) for i in html_item_list]
        data = pd.concat([data,pd.DataFrame(df_scheme)])
    return data


@asset(description='add features and humanize data')
def featuring_data(item_list:pd.DataFrame)->pd.DataFrame:
    data = item_list.copy()
    data['price'] = data['price'].astype(float)
    data['street']= data['adress'].str.extract('(.*?), (?=\d.*)')
    data['is_new']= data['JK'] == ''
    data['n_rooms']=data['title'].str.extract('«(.*?),')
    data['m2'] = data['title'].str.extract(', (\d+).*м²').astype(float)
    data[['floor','max_floor']] = data['title'].str.extract('(\d+/\d+).*эт')[0].str.split('/',expand=True).astype(float)
    data['text'] = data['text'].str.replace('\n','')
    data['rubm2'] = data['price'] / data['m2']
    data.drop(['title','adress'],axis=1,inplace=True)
    return data


@graph(describtion = 'update date graph')
def get_data_graph(urls_list):

    html_data = html_pages(urls_list)
    rent_dataframes = item_list(html_data)
    complete_data = featuring_data(rent_dataframes)
    
    return complete_data
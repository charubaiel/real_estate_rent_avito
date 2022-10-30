import duckdb
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


HEADERS={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

GEKO_DRIVER_PATH = 'repositories/jobs/ops/geckodriver'


def get_item_info(item):
    item_desc = {}
    try:
        item_desc['datetime'] = pd.to_datetime('now',utc=True)
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


def featuring_data(item_list:list)->pd.DataFrame:
    data = pd.DataFrame(item_list)
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


class DatabaseConnection:
    def __init__(self, connection_path: str):
        self.connection =  duckdb.connect(connection_path)
    def query(self,SQL):
        self.connection.execute(SQL)
    def close_conn(self):
        self.connection.close()
    def append_df(self,df:pd.DataFrame,schema:str='RAW'):

        self.connection.execute(f'''
                    CREATE SCHEMA IF NOT EXISTS {schema};
                    CREATE TABLE IF NOT EXISTS {schema}.avito_RE as select * from df TABLESAMPLE 0;
                    INSERT INTO {schema}.avito_RE select * from df;
                    ''')


class SeleniumConnection:
    def __init__(self):
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options.add_argument(f"HEADERS={HEADERS}")
        self.parser = webdriver.Firefox(options=firefox_options,
                                        executable_path=GEKO_DRIVER_PATH)

    def get(self,url):
        self.parser.get(url)
        self.html_data =  self.parser.find_element('xpath',"//*").get_attribute("outerHTML")
        return self.html_data
    
    def close_conn(self):
        self.parser.close()


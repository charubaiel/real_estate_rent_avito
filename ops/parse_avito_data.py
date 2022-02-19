from dagster import op
import pandas as pd
from utils import get_item_info
from bs4 import BeautifulSoup

@op
def get_item_list(html_data):
    bs_data = BeautifulSoup(html_data.text,features='lxml')
    item_list = bs_data.find('div',{'class':'items-items-kAJAg'}).findAll('div',{'data-marker':'item'})
    df_scheme = [get_item_info(i) for i in item_list]
    return pd.DataFrame(df_scheme)


@op
def fix_data(df):
    df['price'] = df['price'].astype(float)
    df['street']=df['adress'].str.extract('(.*?), (?=\d.*)')
    df[['stantion','metro_distance']] = df['metro'].str.split(',',expand=True,n=1)
    df['metro_distance'] = df['metro_distance'].str.strip().str.split(' ',expand=True)[0].str.replace(',','.').astype(float).apply(lambda x: x*1000 if x<100 else x)
    df['n_rooms']=df['title'].str.extract('«(.*?),')
    df['m2'] = df['title'].str.extract(', (\d+).*м²').astype(float)
    df[['floor','max_floor']] = df['title'].str.extract('(\d+/\d+).*эт')[0].str.split('/',expand=True).astype(float)
    df['text'] = df['text'].str.replace('\n','')
    df['rubm2'] = df['price'] / df['m2']
    df['rubm2m'] = df['rubm2'] * df['metro_distance'] / 1000
    df.drop(['title','adress','metro'],axis=1,inplace=True)
    return df


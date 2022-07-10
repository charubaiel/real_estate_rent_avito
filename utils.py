import pandas as pd
import sqlite3


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
        item_desc['fee'] = item.find('span',{'class':'price-noaccent-X6dOy price-textWithoutDiscount-a1bS9 text-text-LurtD text-size-s-BxGpL'}).text
        item_desc['adress'] = item.find('div',{'data-marker':'item-address'}).span.text
        item_desc['metro_dist'] = item.find('span',{'class':'geo-periodSection-bQIE4'}).text
        item_desc['metro'] = item.find('div',{'class':'geo-georeferences-SEtee text-text-LurtD text-size-s-BxGpL'}).text.replace(item_desc['metro_dist'],'')
        item_desc['metro_branch'] = item.find('i',{'class':'geo-icon-Cr9YM'})['style'].replace('background-color:','')
    except:
        pass

    return item_desc

def save_to_db(data,table_name,db_path):
    with sqlite3.connect(db_path) as w:
        pd.DataFrame(data).to_sql(name = table_name,con=w,if_exists='append')


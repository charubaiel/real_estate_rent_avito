from dagster import op
import requests as r
from bs4 import BeautifulSoup

msc_2_3_re = 'https://www.avito.ru/moskva/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1&f=ASgBAQECAUSSA8YQBEDmBxSMUsoIJIRZglmQvg0klK41lq41wMENFLr9NwFFxpoMGHsiZnJvbSI6MCwidG8iOjMwMDAwMDAwfQ&s=104'

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}



@op
def get_avito_page(START_URL_PAGE=msc_2_3_re):
    start_page_html = r.get(START_URL_PAGE,headers=headers)
    if start_page_html.status_code ==200:
        start_page_bs = BeautifulSoup(start_page_html.text,features="lxml")
        return start_page_bs
    else :
        raise ValueError(start_page_bs = BeautifulSoup(start_page_html.text,features="lxml"))

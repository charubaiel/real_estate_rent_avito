from dagster import op ,get_dagster_logger as log
import requests as r



@op()
def get_avito_page1(url):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    start_page_html = r.get(url,headers=headers)

    if start_page_html.status_code == 200:
        log().info(start_page_html.status_code)
        return start_page_html
    else :
        log().info(start_page_html.status_code)



@op()
def get_avito_page2(url):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    start_page_html = r.get(url,headers=headers)

    if start_page_html.status_code == 200:
        log().info(start_page_html.status_code)
        return start_page_html
    else :
        log().info(start_page_html.status_code)



@op()
def get_avito_page3(url):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    start_page_html = r.get(url,headers=headers)

    if start_page_html.status_code == 200:
        log().info(start_page_html.status_code)
        return start_page_html
    else :
        log().info(start_page_html.status_code)

@op()
def get_avito_page4(url):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    start_page_html = r.get(url,headers=headers)

    if start_page_html.status_code == 200:
        log().info(start_page_html.status_code)
        return start_page_html
    else :
        log().info(start_page_html.status_code)

@op()
def get_avito_page5(url):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    start_page_html = r.get(url,headers=headers)

    if start_page_html.status_code == 200:
        log().info(start_page_html.status_code)
        return start_page_html
    else :
        log().info(start_page_html.status_code)

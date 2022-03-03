from dagster import op ,get_dagster_logger as log
import requests as r
import time
import numpy as np
import re







@op()
def get_avito_page1(url,num_pages=1):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    time.sleep(np.random.poisson(15))

    if num_pages<=1:
        start_page_html = r.get(url,headers=headers)

        if start_page_html.status_code == 200:
            log().info(start_page_html.status_code)
            return [start_page_html]
        else :
            raise ValueError(start_page_html.text)
            log().info(start_page_html.status_code)
    else :
        new_p = int(re.findall('p=(\d?)',url)[0])
        htmls = []
        for _ in range(num_pages):
            
            htmls.append(r.get(url.replace(f'&p={new_p}',f'&p={new_p+5}'),headers=headers))
            time.sleep(np.random.poisson(3))
            new_p+=5
        return htmls

@op()
def get_avito_page2(url,num_pages=1):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    time.sleep(np.random.poisson(15*2**1))

    if num_pages<=1:
        start_page_html = r.get(url,headers=headers)

        if start_page_html.status_code == 200:
            log().info(start_page_html.status_code)
            return [start_page_html]
        else :
            raise ValueError(start_page_html.text)
            log().info(start_page_html.status_code)
    else :
        new_p = int(re.findall('p=(\d?)',url)[0])
        htmls = []
        for _ in range(num_pages):
            htmls.append(r.get(url.replace(f'&p={new_p}',f'&p={new_p+5}'),headers=headers))
            time.sleep(np.random.poisson(3))
            new_p+=5
        return htmls



@op()
def get_avito_page3(url,num_pages=1):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    time.sleep(np.random.poisson(15*2**1.5))

    if num_pages<=1:
        start_page_html = r.get(url,headers=headers)

        if start_page_html.status_code == 200:
            log().info(start_page_html.status_code)
            return [start_page_html]
        else :
            raise ValueError(start_page_html.text)
            log().info(start_page_html.status_code)
    else :
        new_p = int(re.findall('p=(\d?)',url)[0])
        htmls = []
        for _ in range(num_pages):
            htmls.append(r.get(url.replace(f'&p={new_p}',f'&p={new_p+5}'),headers=headers))
            time.sleep(np.random.poisson(3))
            new_p+=5
        return htmls

@op()
def get_avito_page4(url,num_pages=1):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    time.sleep(np.random.poisson(15*2**2))

    if num_pages<=1:
        start_page_html = r.get(url,headers=headers)

        if start_page_html.status_code == 200:
            log().info(start_page_html.status_code)
            return [start_page_html]
        else :
            raise ValueError(start_page_html.text)
            log().info(start_page_html.status_code)
    else :
        new_p = int(re.findall('p=(\d?)',url)[0])
        htmls = []
        for _ in range(num_pages):
            htmls.append(r.get(url.replace(f'&p={new_p}',f'&p={new_p+5}'),headers=headers))
            time.sleep(np.random.poisson(3))
            new_p+=5
        return htmls

@op()
def get_avito_page5(url,num_pages=1):
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    time.sleep(np.random.poisson(15*2**2.5))

    if num_pages<=1:
        start_page_html = r.get(url,headers=headers)

        if start_page_html.status_code == 200:
            log().info(start_page_html.status_code)
            return [start_page_html]
        else :
            raise ValueError(start_page_html.text)
            log().info(start_page_html.status_code)
    else :
        new_p = int(re.findall('p=(\d?)',url)[0])
        htmls = []
        for _ in range(num_pages):
            htmls.append(r.get(url.replace(f'&p={new_p}',f'&p={new_p+5}'),headers=headers))
            time.sleep(np.random.poisson(3))
            new_p+=5
        return htmls

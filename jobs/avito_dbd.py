
from ops.parse_avito_data import featuring_data, get_item_list,get_pages
from ops.suppport_funcs import get_urls, save_to_sql
from dagster import job,config_from_files




@job(config=config_from_files(['params/rent_yaml.yaml']))
def parse_avito_data():
    urls_list = get_urls()    
    html_data = get_pages(urls_list)
    rent_dataframes = get_item_list(html_data)
    complete_data = featuring_data(rent_dataframes)
    
    save_to_sql(complete_data)




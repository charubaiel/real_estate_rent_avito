
from repositories.jobs.ops.parse_avito_data import featuring_data, html_pages,item_list,get_data_graph
from repositories.jobs.ops.support_funcs import get_urls, save_to_sql
from dagster import job,config_from_files,schedule





@job(config=config_from_files(['params/rent_yaml.yaml']))
def parse_avito_data():
    urls_list = get_urls()  

    complete_data = get_data_graph(urls_list)

    save_to_sql(complete_data)



@schedule(
    cron_schedule="15 */6 * * *",
    job=parse_avito_data,
    execution_timezone="Europe/Moscow",
)
def avito_schedule():
    return {}
from dagster import asset
from repositories.jobs.ops.support_funcs import (DatabaseConnection,
                                                 SeleniumConnection,
                                                 update_db)


@asset(description='get list of pages to parse')
def get_urls(context) -> str:
    return context.op_config['url']


@asset(description='collect raw html data',)
def fetch_pages(context, get_urls: str) -> None:
    db = DatabaseConnection(context.op_config['db_path'])
    parser = SeleniumConnection()

    for page in range(2, context.op_config['n_pages']+1):

        response = parser.get(get_urls)
        get_urls = get_urls.replace(f'&p={page-1}', f'&p={page}')
        if 'Продажа квартир в Москве' not in parser.parser.find_element('xpath', '//*[@id="app"]/div/div[3]/div[2]').text:
            break
        update_db(response,db_resourse=db)
        parse_stats = db.query('select count(*) as ttl_ads, count(distinct url) as uniq_ads from INTEL.avito_RE ').df()
        context.log.info(
            f'''Parsed pages : {page}/{context.op_config["n_pages"]}
                total ads :{parse_stats.loc[0,'ttl_ads']}
                uniq ads :{parse_stats.loc[0,'uniq_ads']}
            '''
            )
    db.close_conn()
    parser.close_conn()





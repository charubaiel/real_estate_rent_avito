from __init__ import *




parser = argparse.ArgumentParser()

parser.add_argument('-rent','--is_rent',action="store_true",
                    help="scan rent instead of real estate")
args = parser.parse_args()




DB_PATH = r"data/avito_real_estate.db"

TABLE_NAME = "moscow_RE"
START_URL_PAGE = 'https://www.avito.ru/moskva/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1&f=ASgBAQICAUSSA8YQBkDmBxSMUsoIJIRZglnmFhTm_AGQvg0Ulq41rL4NFKTHNcDBDRS6_Tc&p=1'

if args.is_rent:
    
    TABLE_NAME = "moscow_rent"
    START_URL_PAGE = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&f=ASgBAQICAkSSA8gQ8AeQUgNAzAgkjFmOWegWFOj8Aay~DRSkxzU&p=1'


logging.basicConfig(level=logging.INFO,filename=rf'data/{TABLE_NAME}.log',format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


if __name__ == '__main__':

    logging.info('start_scan')

    start_page_html = r.get(START_URL_PAGE)

    start_page = BeautifulSoup(start_page_html.text,features="lxml")

    max_pages = int(start_page.find('div',{'data-marker':'pagination-button'}).findAll('span')[-2].text)

    logging.info(f'max_pages find : {max_pages}')

    err_count = 0

    for i in tqdm(range(1,max_pages)):
        try:
            rng = np.random.poisson(5)
            time.sleep(rng)
            
            qq = r.get(START_URL_PAGE.replace('&p=1',f'&p={i}'))
            
            item_list = get_item_list(qq.text)
            
            page_df = [get_item_info(i) for i in item_list]
            

            save_to_db(pd.DataFrame(page_df),table_name=TABLE_NAME,db_path=DB_PATH)

        except:
            err_count+=1
            logging.error(f'error on {i}th page')

            if err_count ==3 :
                break



    logging.info(f'end of scann')
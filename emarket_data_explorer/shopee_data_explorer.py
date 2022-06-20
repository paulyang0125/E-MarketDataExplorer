#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality.

Todo:\n
1. move to data process\n
2. define the data format of response here\n
3. define and design the consistent responses across all functions between CLI and controller\n
4. decouple mode here as it's used for shopee only, not other data sources
"""
# shopee_data_explorer/shopee_data_explorer.py


from abc import ABC
import asyncio
from typing import Any, Dict, List, NamedTuple, Tuple
import logging
import time
import platform
import pandas as pd
from matplotlib.font_manager import FontProperties
from tqdm import tqdm
from emarket_data_explorer import MODES, CSV_WRITE_ERROR,READ_INDEX_ERROR, READ_PRODUCT_ERROR,\
    READ_COMMENT_ERROR, SUCCESS, EDA_ERROR
import emarket_data_explorer
from emarket_data_explorer import shopee_eda
from emarket_data_explorer.database import DatabaseHandler
from emarket_data_explorer.shopee_crawler import CrawlerHandler
from emarket_data_explorer.data_process import CrawlerDataProcesser
from emarket_data_explorer.shopee_eda import ShopeeEDA
from emarket_data_explorer.shopee_async_crawler import ShopeeAsyncCrawlerHandler


mylogger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
# create console handler with a higher log level
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)


##workflow

class WorkFlow(ABC):
    """the abstract class of workflow"""
    #pass

class ShopeeAsyncWorkFlow(WorkFlow):
    """ the implementation of workflow for shopee async io"""

    def do_workflow_all(self,**kwargs):
    #def do_workflow_all(self,keyword,num_of_product,\
    # page_length,data_source,ip_addresses,proxy_auth,header):
        """ workflow for all """

        #kwargs['ip_addresses']

        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        result = asyncio.run(kwargs['handler'].process_all(kwargs['keyword'], \
            kwargs['num_of_product'],kwargs['page_length'], kwargs['data_source'],
            kwargs['mode']),debug=True)
        #asyncio.run(shopee_handler.process_all(keyword, num_of_product,\
        # page_length, data_source),debug=True)

        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        return result


    def do_workflow_product_info(self,**kwargs):
        """ workflow for product info """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        result = asyncio.run(kwargs['handler'].process_product(kwargs['keyword'],\
            kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
                kwargs['mode']),debug=True)
        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        return result

    def do_workflow_product_comment(self,**kwargs):
        """ workflow for comment """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        result = asyncio.run(kwargs['handler'].process_comment(kwargs['keyword'],\
            kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
                kwargs['mode']),debug=True)
        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        return result

    def do_workflow_product_index(self,**kwargs):
        """ workflow for the index """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        result = asyncio.run(kwargs['handler'].process_index(kwargs['keyword'],\
            kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
                kwargs['mode']),debug=True)
        #shopee_handler = ShopeeAsycCrawlerHandler(ip_addresses=ip_addresses,\
        # proxy_auth=proxy_auth,header=header)
        #merged_search_index_df, ids_pool, status = asyncio.run(shopee_handler.\

        duration = time.time() - start_time
        print(f"Duration {duration} seconds")
        return result



###dataclass
class ScrapingInfo(NamedTuple):
    """ data model to CLI"""
    scraping_info: Dict[str, Any]
    error: int

class ScrapingInfoForList(NamedTuple):
    """ data model for index"""
    scraping_info: List[Dict[str, Any]]
    error: int

class ScrapingInfoForDF(NamedTuple):
    """ data model for dataframe"""
    scraping_info: pd.DataFrame
    error: int


class Explorer:
    """ this class acts as the MVC controller between the implementation of
    crawlers and eda tools, and the CLI interface

    """
    # def __init__(self,data_path:Path,db_path:Path,ip_addresses: List[str], proxy_auth: str,\
    #     my_header: Dict[str, any], webdriver_path:str, data_source:int) -> None:
    def __init__(self,**kwargs) -> None:
        # debug
        #print("1. header type: " + str(type(header)))
        #print("1. header items: " + str(header.items))

        self._crawler_handler = CrawlerHandler(kwargs['ip_addresses'],kwargs['proxy_auth'],\
            kwargs['my_header'],kwargs['webdriver_path'])
        self._async_crawler_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
            proxy_auth=kwargs['proxy_auth'],header=kwargs['my_header'],)
        self._data_processor = CrawlerDataProcesser(kwargs['data_source'])
        self._db_handler = DatabaseHandler(kwargs['data_path'],kwargs['db_path'])
        self.a_page_product_index = []
        self.data_path = kwargs['data_path']
        self.data_source = kwargs['data_source']


    def read_index_selenium(self, keyword: str,page_num: int) -> ScrapingInfo:
        """read the index by selenium"""
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
        }
        read = self._crawler_handler.read_a_page_selenium_search_indexs(keyword,page_num)

        if read.error == READ_INDEX_ERROR:
            return ScrapingInfo(scraper_init, read.error)

        self.a_page_product_index=read.result

        scraper_response = {
            "keyword":keyword,
            "page_num": page_num,
            "obtained_index_num":len(self.a_page_product_index),
        }
        return ScrapingInfo(scraper_response, read.error)


    def read_index_api(self, keyword: str,page_num: int,page_length: int) -> ScrapingInfo:
        """for testing/debug, read the index by shopee api"""
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
        }

        product_items_container = pd.DataFrame()
        for page in tqdm(range(page_num)):
            read = self._crawler_handler.read_search_indexs(keyword,page,page_length)
            if read.error == READ_INDEX_ERROR:
                return ScrapingInfo(scraper_init, read.error)

            # todo: move to data process
            product_items = {}
            #for i in range(len(read.result)):
            for count, _ in enumerate(read.result):
                product_items[count] = read.result[count]['item_basic']
            product_items=pd.DataFrame(product_items).T

            #product_items_container.append(product_items,ignore_index=True)
            #pd.concat([product_items_container,product_items], ignore_index=True, \
            # sort=True, axis=0)
            product_items_container = pd.concat([product_items_container,product_items],axis=0)

        #product_items=pd.DataFrame(read.result)

        scraper_response = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
            "obtained_index_num":len(product_items_container['itemid'].tolist()),
        }
        return ScrapingInfo(scraper_response, read.error)

    def read_index(self, keyword: str,page_num: int,page_length: int) -> ScrapingInfo:
        """read the index by shopee api"""
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
        }
        #product_items_container = pd.DataFrame()
        product_items = []
        for page in tqdm(range(page_num)):
            read = self._crawler_handler.read_search_indexs(keyword,page,page_length)
            if read.error == READ_INDEX_ERROR:
                return ScrapingInfo(scraper_init, read.error)
            # debug
            #print(Explorer.read_index.__name__, "-read.result: ", str(read.result))
            #product_items = {key: value for (key, value) in (product_items.items() + \
            #    read.result.items())}
            product_items.extend(read.result)
            #print(Explorer.read_index.__name__,"-product_items: ", str(product_items))
        #return ScrapingInfo(product_items, read.error)
        return ScrapingInfoForList(product_items, read.error)
    #return ScrapingInfo(product_items_container.to_json(), read.error)



    def read_good_details(self, shop_id: int, item_id: int) -> ScrapingInfo:
        """read good details by shopee api"""
        scraper_init = {
            "shop_id":shop_id,
            "item_id": item_id,
        }
        read = self._crawler_handler.read_good_info(shop_id, item_id)
        if read.error == READ_PRODUCT_ERROR:
            return ScrapingInfo(scraper_init, read.error)
        # debug
        #print(Explorer.read_good_details.__name__, "-read.result: ", str(read.result))
        #good_details = process_product_data(read.result)

        return ScrapingInfo(read.result, read.error)


    def read_good_comments(self,shop_id: int, item_id: int) -> ScrapingInfoForList:
        """read good comments by shopee api"""
        # todo: definte and design the consistent responses between CLI and controller
        #scraper_init = {
        #    "shop_id":shop_id,
        #    "item_id": item_id,
        #}
        read = self._crawler_handler.read_good_comments(shop_id, item_id)
        if read.error == READ_COMMENT_ERROR:
            #return ScrapingInfoForList(scraper_init, read.error)
            return ScrapingInfoForList([{}], read.error)
        #debug
        #print(Explorer.read_good_comments.__name__, "-read.result: ", str(read.result))
        return ScrapingInfoForList(read.result, read.error)

    def _extract_keyword(self,product_csv_name:str) -> str:
        """ extract keyword from the csv name"""
        return product_csv_name.split('_')[1]

    def _extract_source(self,product_csv_name:str) -> str:
        """ extract data source from the csv name"""
        return product_csv_name.split('_')[0]


    def _detect_path_format_for_os(self) -> Tuple[str,str]:
        """ find out the right path format for user os"""
        the_os = list(platform.uname())[0]
        if the_os == 'Windows':
            the_os = '\\'
            os_encode = 'utf-8-sig'
        elif the_os == 'Darwin':
            the_os = '/'
            os_encode = 'utf-8-sig'
        else:
            the_os = '/'
            os_encode = 'utf-8'

        return (the_os,os_encode)


    def do_eda(self, product_csv_name:str, product_comment_name:str)-> shopee_eda.EDAResponse:
        """the main entry of EDA command that will generate 6 EDA charts with the pre-process """
        the_os, os_encode = self._detect_path_format_for_os()
        my_font = FontProperties(fname='tools'+ the_os + 'msj.ttf')
        product_csv_name_path = self.data_path.joinpath(product_csv_name)
        product_comment_name_path = self.data_path.joinpath(product_comment_name)
        #os.chdir(self.data_path)

        #if os.path.exists(product_csv_name) and os.path.exists(product_comment_name):
        if product_csv_name_path.exists() and product_comment_name_path.exists():
            products_data = pd.read_csv(product_csv_name_path,encoding = os_encode, \
                engine= 'python')
            comments_data = pd.read_csv(product_comment_name_path,encoding = os_encode, \
                engine= 'python')
            chart_groups = ['make_figure1', 'make_figure2', 'make_figure3','make_figure4',\
            'make_figure5', 'make_figure6']
            keyword = self._extract_keyword(product_csv_name)
            data_source = self._extract_source(product_csv_name)
            shopee_eda_instance = ShopeeEDA(keyword=keyword,data_source=data_source,\
                data_path=self.data_path,chart_groups=chart_groups,\
                product_data=products_data,comments_data=comments_data,my_font=my_font,\
                chart_color=None)
            read = shopee_eda_instance.do_eda()
            #todo: define the data format of response here
            return (read.result,SUCCESS)
        else:
            print(f"{product_csv_name} or {product_comment_name} is not found in {self.data_path}")
            #raise sys.exit(1)
            return (read.result,EDA_ERROR)


    def scrap(self, keyword: str, num_of_product: int, mode:int, page_length:int\
        ) -> ScrapingInfo:
        """the main entry of scrap command that scraps data source with the specified
           number of the result based on mode suer select.\n

           page length is 50 here by default so suppose user should input multiplier of 50
           otherwise use floor division that rounds any number down to the nearest integer,
           so if 256 is given, the page should be 5 that will miss extra 6 items.\n

        """
        # todo: decouple mode here as it's used for shopee only, not other data sources

        # page length is 50 here by default so suppose user should input multiplier of 50
        # otherwise use floor division - // rounds any number down to the nearest integer.
        # so if 256 is given, the page should be 5 that will miss extra 6 items

        #page_length = shopee_crawler.DEFAULT_PAGE_LENGTH
        #self.keyword = keyword
        page_num = num_of_product // page_length
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
        }
        # product_items_container is the aggregator of product data
        product_items_container = pd.DataFrame()
        product_comments_container = pd.DataFrame()

        for page in tqdm(range(page_num), position=0, leave=True):
            read = self._crawler_handler.read_search_indexs(keyword,page,page_length)
            if read.error == READ_INDEX_ERROR:
                return ScrapingInfo(scraper_init, read.error)
            product_items = self._data_processor.process_raw_search_index(read.result)


            for index, (item_id, shop_id, name) in tqdm(enumerate(zip(product_items['itemid']\
                .tolist(),\
                product_items['shopid'].tolist(),product_items['name'].tolist())),\
                total=len(product_items['itemid'].tolist()), position=0, leave=True):

                mylogger.info('# %i,scarping %s ...', index, name[:30])

                if mode == emarket_data_explorer.ALL or mode == emarket_data_explorer.\
                    PRODUCT_ITEMS:
                    read=self.read_good_details(shop_id = shop_id, item_id=item_id)
                    # test: fix by ['item']. maybe it's not a better place to put it
                    product = read.scraping_info['item']
                    self._data_processor.process_product_data(product)

                if mode == emarket_data_explorer.ALL or mode == emarket_data_explorer.\
                    PRODUCT_COMMENTS:
                    read = self.read_good_comments(shop_id = shop_id, item_id=item_id)
                    comment = read.scraping_info
                    product_comments_container = self._data_processor.process_comment_data\
                        (comment,product_comments_container)

            #debug
            #print("scrapall->container:head", product_items_container.head(5))
            #print("scrapall->container:tail", product_items_container.tail(5))
            #print("scrapall->comment_container:head", product_comments_container.head(5))
            #print("scrapall->comment_container:tail", product_comments_container.tail(5))

            if mode == emarket_data_explorer.ALL or mode == emarket_data_explorer.\
                    PRODUCT_ITEMS:
                product_items_container = self._data_processor.aggregate_product_data\
                    (product_items_container,product_items)
                self._data_processor.clean_product_data()
                crawler_mode = MODES[mode]
                if mode == emarket_data_explorer.ALL:
                    crawler_mode = crawler_mode.split(':')[0]

                read = self._db_handler.write_csv(product_items_container, keyword,\
                    self.data_source,crawler_mode)

                if read.error == CSV_WRITE_ERROR:
                    return ScrapingInfo(read.response.to_dict(), read.error)
                #self._data_processor.write_shopee_goods_data(product_items_container, keyword)
            #debug
            #print("after:scrapall->container:head", product_items_container.head(5))
            #print("after:scrapall->container:tail", product_items_container.tail(5))
            if mode == emarket_data_explorer.ALL or mode == emarket_data_explorer.\
                    PRODUCT_COMMENTS:

                crawler_mode = MODES[mode]
                if mode == emarket_data_explorer.ALL:
                    crawler_mode = crawler_mode.split(':')[1]

                read = self._db_handler.write_csv(product_comments_container, keyword,\
                    self.data_source,crawler_mode)
                if read.error == CSV_WRITE_ERROR:
                    return ScrapingInfo(read.response.to_dict(), read.error)
                #self._data_processor.write_shopee_comments_data(product_comments_container,\
                #  keyword)

        if mode == emarket_data_explorer.ALL:
            if not product_items_container.empty and not product_comments_container.empty:
                scraper_response = {
                "keyword":keyword,
                "page_num": page_num,
                "page_length":page_length,
                "obtained_product_num":len(product_items_container.index),
                "obtained_comment_num":len(product_comments_container.index),
                }

                return ScrapingInfo(scraper_response, read.error)
            else:
                print("containers are empty")
                return ScrapingInfo(scraper_init, read.error)

        elif mode == emarket_data_explorer.PRODUCT_ITEMS:
            if not product_items_container.empty:
                scraper_response = {
                "keyword":keyword,
                "page_num": page_num,
                "page_length":page_length,
                "obtained_product_num":len(product_items_container.index),
                }

                return ScrapingInfo(scraper_response, read.error)
            else:
                print("containers are empty")
                return ScrapingInfo(scraper_init, read.error)

        elif mode == emarket_data_explorer.PRODUCT_COMMENTS:
            if not product_comments_container.empty:
                scraper_response = {
                "keyword":keyword,
                "page_num": page_num,
                "page_length":page_length,
                "obtained_comment_num":len(product_comments_container.index),
                }

                return ScrapingInfo(scraper_response, read.error)
            else:
                print("containers are empty")
                return ScrapingInfo(scraper_init, read.error)

    def scrap_async(self, keyword: str, num_of_product: int, mode:int,\
        page_length:int) -> ScrapingInfo:
        """ async version of scraping"""

        workflower = ShopeeAsyncWorkFlow()
        #scrap_params = {}
        #scrap_params['keyword'] = keyword
        #scrap_params['num_of_product'] = num_of_product

        if mode == emarket_data_explorer.ALL:
            workflower.do_workflow_all(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode)

        if mode == emarket_data_explorer.PRODUCT_ITEMS:
            workflower.do_workflow_product_info(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode)

        if mode == emarket_data_explorer.PRODUCT_COMMENTS:
            workflower.do_workflow_product_comment(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode)

        if mode == emarket_data_explorer.PRODUCT_INDEXES:
            workflower.do_workflow_product_index(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode)

        return SUCCESS
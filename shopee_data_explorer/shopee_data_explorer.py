#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality."""
# shopee_data_explorer/shopee_data_explorer.py
# rptodo/rptodo.py
#from pathlib import Path
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import logging
import pandas as pd
from tqdm import tqdm
from shopee_data_explorer import MODES, CSV_WRITE_ERROR,READ_INDEX_ERROR, READ_PRODUCT_ERROR,\
    READ_COMMENT_ERROR
import shopee_data_explorer
from shopee_data_explorer.database import DatabaseHandler
from shopee_data_explorer.shopee_crawler import CrawlerHandler
from shopee_data_explorer.data_process import CrawlerDataProcesser


mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f'{__name__}.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)


class ScrapingInfo(NamedTuple):
    """ data model to CLI"""
    scraping_info: Dict[str, Any]
    error: int

class ScrapingInfoForList(NamedTuple):
    """ data model for index"""
    scraping_info: List[Dict[str, Any]]
    error: int

class ScrapingInfoForDF(NamedTuple):
    """ data model for index"""
    scraping_info: pd.DataFrame
    error: int


class Explorer:
    """ test """
    def __init__(self,data_path:Path,db_path:Path,ip_addresses: List[str], proxy_auth: str,\
        header: Dict[str, any], webdriver_path:str, data_source:int) -> None:
        # debug
        print("1. header type: " + str(type(header)))
        print("1. header items: " + str(header.items))
        self._crawler_handler = CrawlerHandler(ip_addresses,proxy_auth,header,webdriver_path)
        self._data_processor = CrawlerDataProcesser(data_source)
        self._db_handler = DatabaseHandler(data_path,db_path)
        self.a_page_product_index = []
        self.data_path = data_path
        self.data_source = data_source

    def read_index_selenium(self, keyword: str,page_num: int) -> ScrapingInfo:
        """read the index"""
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
        """read the index"""
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
        """read the index"""
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
        """test"""
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
        """test"""
        '''
        scraper_init = {
            "shop_id":shop_id,
            "item_id": item_id,
        }
        '''
        read = self._crawler_handler.read_good_comments(shop_id, item_id)
        if read.error == READ_COMMENT_ERROR:
            #return ScrapingInfoForList(scraper_init, read.error)
            return ScrapingInfoForList([{}], read.error)
        #debug
        #print(Explorer.read_good_comments.__name__, "-read.result: ", str(read.result))
        return ScrapingInfoForList(read.result, read.error)


    def scrap(self, keyword: str, num_of_product: int, mode:int, page_length:int\
        ) -> ScrapingInfo:
        """tests"""
        # page length is 50 here by default so suppose user should input multiplier of 50
        # otherwise use floor division - // rounds any number down to the nearest integer.
        # so if 256 is given, the page should be 5 that will miss extra 6 items

        #page_length = shopee_crawler.DEFAULT_PAGE_LENGTH

        page_num = num_of_product // page_length
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
        }
        # product_items_container is the aggrgator of product data
        product_items_container = pd.DataFrame()
        product_comments_container = pd.DataFrame()

        for page in tqdm(range(page_num)):
            read = self._crawler_handler.read_search_indexs(keyword,page,page_length)
            if read.error == READ_INDEX_ERROR:
                return ScrapingInfo(scraper_init, read.error)
            product_items = self._data_processor.process_raw_search_index(read.result)


            for item_id, shop_id, name in tqdm(zip(product_items['itemid'].tolist(),\
                product_items['shopid'].tolist(),product_items['name'].tolist()),\
                total=len(product_items['itemid'].tolist())):
                mylogger.info('scaraping %s ...', name[:30])

                if mode == shopee_data_explorer.ALL or mode == shopee_data_explorer.\
                    PRODUCT_ITEMS:
                    read=self.read_good_details(shop_id = shop_id, item_id=item_id)
                    # test: fix by ['item']. maybe it's not a better place to put it
                    product = read.scraping_info['item']
                    self._data_processor.process_product_data(product)

                if mode == shopee_data_explorer.ALL or mode == shopee_data_explorer.\
                    PRODUCT_COMMENTS:
                    read = self.read_good_comments(shop_id = shop_id, item_id=item_id)
                    comment = read.scraping_info
                    product_comments_container = self._data_processor.process_comment_data\
                        (comment,product_comments_container)

            #debug
            #print("scrapall->conatiner:head", product_items_container.head(5))
            #print("scrapall->conatiner:tail", product_items_container.tail(5))
            #print("scrapall->comment_conatiner:head", product_comments_container.head(5))
            #print("scrapall->comment_conatiner:tail", product_comments_container.tail(5))

            if mode == shopee_data_explorer.ALL or mode == shopee_data_explorer.\
                    PRODUCT_ITEMS:
                product_items_container = self._data_processor.aggregate_product_data\
                    (product_items_container,product_items)
                self._data_processor.clean_product_data()
                crawler_mode = MODES[mode]
                if mode == shopee_data_explorer.ALL:
                    crawler_mode = crawler_mode.split(':')[0]

                read = self._db_handler.write_csv(product_items_container, keyword,\
                    self.data_source,crawler_mode)

                if read.error == CSV_WRITE_ERROR:
                    return ScrapingInfo(read.response.to_dict(), read.error)
                #self._data_processor.write_shopee_goods_data(product_items_container, keyword)
            #debug
            #print("after:scrapall->conatiner:head", product_items_container.head(5))
            #print("after:scrapall->conatiner:tail", product_items_container.tail(5))
            if mode == shopee_data_explorer.ALL or mode == shopee_data_explorer.\
                    PRODUCT_COMMENTS:

                crawler_mode = MODES[mode]
                if mode == shopee_data_explorer.ALL:
                    crawler_mode = crawler_mode.split(':')[1]

                read = self._db_handler.write_csv(product_comments_container, keyword,\
                    self.data_source,crawler_mode)
                if read.error == CSV_WRITE_ERROR:
                    return ScrapingInfo(read.response.to_dict(), read.error)
                #self._data_processor.write_shopee_comments_data(product_comments_container,\
                #  keyword)

        if mode == shopee_data_explorer.ALL:
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

        elif mode == shopee_data_explorer.PRODUCT_ITEMS:
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

        elif mode == shopee_data_explorer.PRODUCT_COMMENTS:
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







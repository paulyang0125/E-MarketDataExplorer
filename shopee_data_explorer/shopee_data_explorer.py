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
from typing import Any, Dict, List, NamedTuple
import pandas as pd
from tqdm import tqdm
from shopee_data_explorer import READ_INDEX_ERROR
from shopee_data_explorer.shopee_crawler import CrawlerHandler



class ScrapingInfo(NamedTuple):
    """ data model to CLI"""
    scraping_info: Dict[str, Any]
    error: int

class Explorer:
    """ test """
    def __init__(self, ip_addresses: List[str], proxy_auth: str, \
    header: Dict[str, any],path:str) -> None:
        self._crawler_handler = CrawlerHandler(ip_addresses,proxy_auth,header,path)
        self.a_page_product_index = []

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
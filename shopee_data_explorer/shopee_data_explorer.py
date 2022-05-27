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
from shopee_data_explorer import READ_INDEX_ERROR
from shopee_data_explorer.shopee_crawler import CrawlerHandler
import pandas as pd


class ScrapingInfo(NamedTuple):
    """ data model to CLI"""
    scraping_info: Dict[str, Any]
    error: int

class Explorer:
    """ test """
    def __init__(self, ip_addresses: List[str], proxy_auth: str, \
    header: Dict[str, any]) -> None:
        self._crawler_handler = CrawlerHandler(ip_addresses,proxy_auth,header)

    def read_index(self, keyword: str,page_num: int,page_length: int) -> ScrapingInfo:
        """read the index"""
        scraper_init = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
        }
        read = self._crawler_handler.read_good_indexs(keyword,page_num,page_length)

        if read.error == READ_INDEX_ERROR:
            return ScrapingInfo(scraper_init, read.error)

        product_items=pd.DataFrame(read.result)

        scraper_response = {
            "keyword":keyword,
            "page_num": page_num,
            "page_length":page_length,
            "obtained_index_num":str(len(product_items['itemid'].tolist())),
        }
        return ScrapingInfo(scraper_response, read.error)


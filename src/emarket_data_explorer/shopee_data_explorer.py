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

import os
from typing import Tuple
import logging

import platform
import pandas as pd
from matplotlib.font_manager import FontProperties
from emarket_data_explorer import SUCCESS, EDA_ERROR
import emarket_data_explorer
from emarket_data_explorer import shopee_eda
from emarket_data_explorer.shopee_eda import ShopeeEDA
from emarket_data_explorer.shopee_async_crawler import ShopeeAsyncCrawlerHandler
from emarket_data_explorer.data_process import ShopeeAsyncCrawlerDataProcesser
from emarket_data_explorer.database import ShopeeAsyncDatabaseHandler
from emarket_data_explorer.datatype import ScrapingInfo
from emarket_data_explorer.workflow import ShopeeAsyncWorkFlow
from emarket_data_explorer.classtype import Explorer


# def load_msj():
#     try:
#         import importlib.resources as pkg_resources, resource
#     except ImportError:
#         # Try backported to PY<37 `importlib_resources`.
#         import importlib_resources as pkg_resources
#     #from pkg_resources import resource_string as resource_bytes
#     from . import tools
#     #word_file = resource_bytes(tools, 'msj.ttf')
#     word_file = resource.open_binary(tools, 'msj.ttf')
#     return word_file

# def load_msj_1():
#     import pkgutil
#     from . import tools
#     #word_file = resource_bytes(tools, 'msj.ttf')
#     word_file = pkgutil.get_data(__name__, "tools/msj.ttf")
#     return word_file



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


def get_path():
    import emarket_data_explorer
    src_path = os.path.dirname(emarket_data_explorer.__file__)
    return src_path



class ShopeeExplorer(Explorer):
    """ this class acts as the MVC controller between the implementation of
    crawlers and eda tools, and the CLI interface

    """
    # def __init__(self,data_path:Path,db_path:Path,ip_addresses: List[str], proxy_auth: str,\
    #     my_header: Dict[str, any], webdriver_path:str, data_source:int) -> None:
    def __init__(self,**kwargs) -> None:
        # debug
        #print("1. header type: " + str(type(header)))
        #print("1. header items: " + str(header.items))

        ### remove ###


        ### remove ###


        ### remove ###

        ### remove ###
        #self.owd = os.getcwd()
        #print(f"explorer self.owd:{self.owd}")
        self.src_path = get_path()
        #self.word_file = load_msj_1()

        self._shopee_async_data_processor = ShopeeAsyncCrawlerDataProcesser(kwargs['data_source'])
        self._shopee_async_db_handler = ShopeeAsyncDatabaseHandler(kwargs['data_path']\
            ,kwargs['db_path'])

        self._async_crawler_handler = ShopeeAsyncCrawlerHandler(ip_addresses=\
            kwargs['ip_addresses'],proxy_auth=kwargs['proxy_auth'],header=kwargs['my_header'],\
                data_handler = self._shopee_async_data_processor)


        self.a_page_product_index = []
        self.data_path = kwargs['data_path']
        self.data_source = kwargs['data_source']

    ### remove ###

    ### remove ###

    ### remove ###

    ### remove ###

    ### remove ###


    ### remove ###

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
        word_file = self.src_path + the_os + 'tools'+ the_os + 'msj.ttf'
        #my_font = FontProperties(fname='tools'+ the_os + 'msj.ttf')
        my_font = FontProperties(fname=word_file)
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

    ### remove ###


    ### remove ###


    def scrap_async(self, keyword: str, num_of_product: int, mode:int,\
        page_length:int) -> ScrapingInfo:
        """ the main entry of async version of scraping"""

        work_flower = ShopeeAsyncWorkFlow()
        #scrap_params = {}
        #scrap_params['keyword'] = keyword
        #scrap_params['num_of_product'] = num_of_product

        if mode == emarket_data_explorer.ALL:
            result = work_flower.do_workflow_all(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.\
                    data_source,mode=mode,data_processor=\
                        self._shopee_async_data_processor,\
                            database=self._shopee_async_db_handler)
                    #kwargs['data_processor'],kwargs['database']
                    #return (ids_pool,[status_index,status_product,status_comment])

        if mode == emarket_data_explorer.PRODUCT_ITEMS:
            result = work_flower.do_workflow_product_info(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode,data_processor=\
                        self._shopee_async_data_processor,\
                            database=self._shopee_async_db_handler) \
                                #return (ids_pool,[status_index,status_product])

        if mode == emarket_data_explorer.PRODUCT_COMMENTS:
            result = work_flower.do_workflow_product_comment(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode,data_processor=\
                        self._shopee_async_data_processor,\
                            database=self._shopee_async_db_handler) \
                                #return (ids_pool,[status_index,status_comment])

        if mode == emarket_data_explorer.PRODUCT_INDEXES:
            result = work_flower.do_workflow_product_index(handler=self._async_crawler_handler,\
                 keyword=keyword,num_of_product=num_of_product,\
                page_length=page_length,data_source=self.data_source,mode=mode,data_processor=\
                        self._shopee_async_data_processor,\
                            database=self._shopee_async_db_handler) \
                                #return (ids_pool,[status_index])

        #todo: this is not tested yet and also not implemented
        #if not result:
        #    return EMPTY_SCRAP_ERROR

        return result # in scrap, it returns ScrapingInfo(scraper_response, read.error)


        # scraper_response = {
        #     "keyword":keyword,
        #     "page_num": page_num,
        #     "page_length":page_length,
        #     "obtained_product_num":len(product_items_container.index),
        #     "obtained_comment_num":len(product_comments_container.index),
        #     }

        # or
        #scraper_response = {
        #    "keyword":keyword,
        #    "page_num": page_num,
        #    "page_length":page_length,
        #    "obtained_comment_num":len(product_comments_container.index),
        #    }

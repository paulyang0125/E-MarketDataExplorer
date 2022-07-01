#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 20/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Async Crawler functionality.

Todo:\n

"""
# shopee_data_explorer/shopee_async_crawler.py

import asyncio
import os
import random
import time
import logging
from typing import Any, Dict, List,Tuple
import aiohttp
import pandas as pd
from tqdm import tqdm
#from async_retrying import retry
from emarket_data_explorer.classtype import CrawlerHandler
import emarket_data_explorer
from emarket_data_explorer import (MODES, READ_INDEX_ERROR)
from emarket_data_explorer.datatype import AsyncCrawlerResponse
from emarket_data_explorer.data_process import ShopeeAsyncCrawlerDataProcesser

### logger
mylogger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)


class ShopeeAsyncCrawlerHandler(CrawlerHandler):
    """ this provides crawler capabilities to read data from shopee """

    def __init__(self, ip_addresses:List[str],proxy_auth:str,header:Dict[str,Any],\
        data_handler:ShopeeAsyncCrawlerDataProcesser) -> None:
        super().__init__(ip_addresses,proxy_auth)
        self.header = header
        self.timeout = 25
        self.ids_pool =[]
        #self.search_results_urls =[]
        self.product_articles = [] #will remove
        self.product_sku = [] #will remove
        self.product_tags = [] #will remove
        self.product_items_container = pd.DataFrame()
        self.product_comments_container = pd.DataFrame()
        #self.mode = mode #will remove just temp for this big class - all

        self.parsing_candidates = {}
        self.parsing_candidates['parse_search_indexs'] = data_handler.parse_search_indexs
        self.parsing_candidates['parse_good_info'] = data_handler.parse_good_info
        self.parsing_candidates['parse_good_comments'] = data_handler.parse_good_comments

        self.data_path = os.chdir(os.getcwd()) #will remove

    async def _fetch(self, session:aiohttp.ClientSession, url:str,\
        parsing_func:ShopeeAsyncCrawlerDataProcesser) -> List[Dict[str, Any]]:
        """ fetch data from url using the aiohttp session with the parsing functions """

        aio_proxies = self._rotate_ip()
        timeout = aiohttp.ClientTimeout(total=25)
        mylogger.debug("start fetching")
        tries = 0

        while tries < 3:
            mylogger.debug("proxy: %s",aio_proxies['http'])
            try:
                start = time.monotonic()
                async with session.get(url, headers=self.header,proxy=aio_proxies['http'],\
                    timeout=timeout,raise_for_status=True) as response:
                    if response.status == 200:
                        mylogger.debug('each duration: %d',time.monotonic() - start)
                        mylogger.debug("Read %i bytes from %s",len(await response.read()),url)

                        text = await response.text()

                        parsed_result = parsing_func(text)

                        return parsed_result
                    else:
                        mylogger.warning("response.status: {response.status}")
                        tries += 1
                        aio_proxies = self._rotate_ip()

            except Exception as error:
                mylogger.warning('My Connection Error %s', str(error))
                if tries < 3:
                    aio_proxies = self._rotate_ip()
                else:
                    return

            tries += 1

    async def _download_all_sites(self, sites:List[str],\
         parse_func:ShopeeAsyncCrawlerDataProcesser) -> List[List[Dict[str, Any]]]:
        """ this is distributor function of async task to feed _fetch func """
        results = []
        async with aiohttp.ClientSession() as session:
            logging.info("Starting to create the session")
            tasks = []
            for url in sites: #for url in tqdm.asyncio(sites,total=len(sites), position=0, leave=True):
                task = asyncio.ensure_future(self._fetch(session,url,parse_func))
                tasks.append(task)

            for future in tqdm(asyncio.as_completed(tasks),\
                total=len(sites), position=0, leave=True, desc="scrap content"):
                result = await future
                results.append(result)
            return results #return await asyncio.gather(*tasks, return_exceptions=True)

    def _rotate_ip(self) -> None:
        """ rotate the current IP from the list of proxy ip addresses """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        return {
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}",
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}"}


    def read_search_indexs_url(self,keyword: str, page: int, page_length: int) -> str:
        """ create the index url based on shopee api """
        page = page + 1
        url = 'https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword=' \
            + keyword + '&limit=' + str(page_length) + '&newest=' + str(page*page_length) + \
                '&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'
        return url

    def read_good_info_url(self,shop_id: int, item_id: int) -> str :
        """ create the product url based on shopee api  """
        url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(item_id) + '&shopid=' + \
                str(shop_id)
        return url

    def read_good_comments_url(self, shop_id: int, item_id: int) -> str :
        """ create the comment url based on shopee api  """
        url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(item_id) + '&shop_id=' + \
            str(shop_id) + '&offset=0&limit=200&flag=1&filter=0'
        return url

    def split_list(self, alist:List[str], wanted_parts:int=1) -> List[List[str]]:
        """ divide the number of task into the multiplier
        of wanted_parts, like f([100]) becomes [[50],[50]]
        """
        length = len(alist)

        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    async def scrap_index(self,kwargs:Dict[str,Any]) \
        ->  Tuple[pd.DataFrame,List[tuple], List[int]]:
        """ read the search result by shopee api """
        mylogger.info("scrap_index starts")
        ###### index
        read_search_indexs_urls = [self.read_search_indexs_url(kwargs['keyword'],\
            page,kwargs['page_length']) for page \
                in range(kwargs['page_nums'])]

        search_index_results = await asyncio.gather(self._download_all_sites(\
            read_search_indexs_urls,self.parsing_candidates['parse_search_indexs']))

        #todo: set_error_check for search_index_results
        # if len(search_index_results[0]) != kwargs['page_nums'] -? - warning
        # if search_index_results[0] is none - critical

        if not search_index_results[0]:
            return pd.DataFrame(), [], READ_INDEX_ERROR

        if len(search_index_results[0]) != kwargs['page_nums']:
            mylogger.warning("read_index_number: %i doesn't match with what we expect :%i",\
                len(search_index_results[0]), kwargs['page_nums'])

        mylogger.debug("how many index: %i",len(search_index_results[0]))

        ### start parsing
        processed_index_dfs = [kwargs['data_processor'].process_raw_search_index(each) for each in \
            search_index_results[0] if search_index_results[0]]

        merged_search_index_df = pd.concat(processed_index_dfs)
        merged_search_index_df = merged_search_index_df.drop_duplicates(subset=['itemid'])

        self.ids_pool.append([(item_id, shop_id, name) for \
            item_id, shop_id, name in zip(merged_search_index_df['itemid'].tolist(),\
                        merged_search_index_df['shopid'].tolist(),\
                                merged_search_index_df['name'].tolist())])
        #shopee,will remove
        if kwargs['mode'] == emarket_data_explorer.ALL:
            crawler_mode = MODES[kwargs['mode']].split(':')[2]
        else:
            crawler_mode = MODES[kwargs['mode']]

        mylogger.debug("index.crawler_mode: %s ", crawler_mode)
        ### write data
        mylogger.info('start writing - product')
        #self.write_csv(merged_search_index_df,keyword,data_source,crawler_mode)
        write_csv_status = kwargs['database'].write_csv(merged_search_index_df,kwargs['keyword'],\
           kwargs['data_source'],crawler_mode)

        # if write_csv_status != SUCCESS:
        #     return merged_search_index_df, self.ids_pool, write_csv_status

        return merged_search_index_df, self.ids_pool, write_csv_status

    #async def scrap_comment(self,ids_pool,keyword,page_nums,data_source,mode):

    async def scrap_comment(self,ids_pool:List[tuple],kwargs:Dict[str,Any]) \
        -> Tuple[pd.DataFrame,List[int]]:
        """ get the buyer's comment by using item_id and shop_id by shopee api """

        mylogger.info("scrap_comment starts")
        ## create urls

        search_comments_urls = []
        #for pages in ids_pool:
        for pages in ids_pool:
            for item in pages: # item is tutle
                search_comments_urls.append(self.read_good_comments_url(item[1],item[0]))

        ## start crawler
        mylogger.info('start crawler - comment')
        comments_list = []
        #sites_lists = self.split_list(search_comments_urls, wanted_parts=page_nums)
        sites_lists = self.split_list(search_comments_urls, wanted_parts=kwargs['page_nums'])
        for sites in sites_lists:
            the_comment_results = await asyncio.gather(self._download_all_sites(sites,\
                            self.parsing_candidates['parse_good_comments']))
            comments_list.append(the_comment_results)

        mylogger.debug("how many good comment: %i", len(comments_list))

        ### start parsing
        mylogger.info('start parsing - comment ')
        start_time = time.time()
        #my_list3[0][0][0],[0]
        for each_loop in tqdm(comments_list,total=len(comments_list),\
            position=0, leave=True, desc="parse comments loop"):
            for each_product in tqdm(each_loop[0],total=len(each_loop[0]),\
                 position=0, leave=True, desc="parse comments"):
                #product_comments_container = self.update_comment_data(each_product)
                product_comments_container = kwargs['data_processor'].\
                    update_comment_data(each_product)

        if kwargs['mode'] == emarket_data_explorer.ALL:
            crawler_mode = MODES[kwargs['mode']].split(':')[1]
        else:
            crawler_mode = MODES[kwargs['mode']]

        mylogger.debug("comment.crawler_mode: %s", crawler_mode)
        duration = time.time() - start_time
        mylogger.debug("Parsing Duration %d seconds", duration)
        #crawler_mode = get_crawler_mode(mode)
        ### write data
        mylogger.info('start writing - comment ')
        #self.write_csv(product_comments_container,keyword,data_source,crawler_mode)
        write_csv_status = kwargs['database'].write_csv(product_comments_container,kwargs['keyword'],\
            kwargs['data_source'],crawler_mode)
        return (product_comments_container , write_csv_status)


    async def scrap_product_info(self,ids_pool:List[tuple],merged_search_index_df:pd.DataFrame,\
        kwargs:Dict[str,Any]) -> Tuple[pd.DataFrame,List[int]]:
        """ get the good details like articles and SKU by shopee api """
        mylogger.info("scrap_product_info starts")
         ## create urls
        search_results_urls =[]
        #for pages in ids_pool:
        for pages in ids_pool:
            for item in pages: # item is tutle \
                #print(item[0],item[1],item[2]) #'itemid', 'shopid', 'name'
                search_results_urls.append(self.read_good_info_url(item[1],item[0]))

        ## start crawler
        product_list = []
        mylogger.info('start crawler - product')
        sites_lists = self.split_list(search_results_urls, wanted_parts=kwargs['page_nums'])
        for sites in sites_lists:
            the_product_results = await asyncio.gather(self._download_all_sites(sites,\
                                    self.parsing_candidates['parse_good_info']))
            product_list.append(the_product_results)

        mylogger.debug("how many good info %d", len(product_list))


        ### start parsing
        mylogger.info('start parsing - product')
        start_time = time.time()
        #my_list2[0][0][0]['item']
        for each_loop in product_list:
            for each_page in each_loop[0]:
                #self.extract_product_data(each_page)
                kwargs['data_processor'].extract_product_data(each_page)

        self.product_items_container = kwargs['data_processor'].aggregate_product_data(self.\
            product_items_container,merged_search_index_df)

        #self.clean_product_data()
        kwargs['data_processor'].clean_product_data()

        if kwargs['mode'] == emarket_data_explorer.ALL:
            crawler_mode = MODES[kwargs['mode']].split(':')[0]
        else:
            crawler_mode = MODES[kwargs['mode']]


        mylogger.debug("product.crawler_mode: %s",crawler_mode )

        duration = time.time() - start_time
        mylogger.debug("Parsing Duration %d seconds", duration)
        ### write data
        mylogger.info('start writing - product')
        write_csv_status = kwargs['database'].write_csv(self.product_items_container,kwargs['keyword'],\
            kwargs['data_source'],crawler_mode)

        return (self.product_items_container, write_csv_status)

    def get_page(self,num_of_product:int,page_length:int) -> int:
        """ get the page of the amount of items to be scrapped """
        page_nums = num_of_product // page_length
        return page_nums


    async def process_all(self,kwargs:Dict[str,Any]) -> AsyncCrawlerResponse:
        """ the entry function to be called by a workflow class for ALL mode """

        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)

        if status_index == READ_INDEX_ERROR or len(ids_pool) == 0:
             #my_return = AsyncCrawlerResponse({},[status_index])
            return AsyncCrawlerResponse({},[status_index])
        ###### productinfo
        (product_items_container, status_product) = await self.scrap_product_info(ids_pool,\
                        merged_search_index_df,kwargs)

        ###### productcomment
        (product_comments_container, status_comment) = await self.scrap_comment(ids_pool,kwargs)

        result_dict = {}
        result_dict['ids_pool'] = ids_pool
        result_dict['merged_search_index_df'] = merged_search_index_df
        result_dict['product_items_container'] = product_items_container
        result_dict['product_comments_container'] = product_comments_container
        my_return = AsyncCrawlerResponse(result_dict,[status_index,status_product,status_comment])

        return my_return

        # return (ids_pool,merged_search_index_df,product_items_container,\
        #     product_comments_container,[status_index,status_product,status_comment])
        #return AsyncCrawlerResponse(result_dict,[status_index,status_product,status_comment])
        #return (result_dict,[status_index,status_product,status_comment])
        #return (ids_pool,[status_index,status_product,status_comment])

    #async def process_product(self,keyword,num_of_product,page_length,data_source,mode):
    async def process_product(self,kwargs:Dict[str,Any]) -> AsyncCrawlerResponse:
        """ the entry function to be called by a workflow class for product mode """
        ###### index

        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)
        if status_index == READ_INDEX_ERROR or len(ids_pool) == 0:
            return AsyncCrawlerResponse({},[status_index])

        ###### productinfo

        (product_items_container, status_product) = await self.scrap_product_info(ids_pool,\
                    merged_search_index_df,kwargs)


        result_dict = {}
        result_dict['ids_pool'] = ids_pool
        result_dict['merged_search_index_df'] = merged_search_index_df
        result_dict['product_items_container'] = product_items_container
        my_return = AsyncCrawlerResponse(result_dict,[status_index,status_product])

        return my_return

        # return (ids_pool,merged_search_index_df,product_items_container,\
        #     [status_index,status_product])
        #return (ids_pool,[status_index,status_product])



    async def process_comment(self,kwargs:Dict[str,Any]) -> AsyncCrawlerResponse:
        """ the entry function to be called by a workflow class for comment mode """

        ###### index

        # page_nums = self.get_page(num_of_product,page_length)
        # merged_search_index_df, ids_pool, status_index = await self.scrap_index(
        #                     keyword,page_nums,page_length,data_source,mode)
        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)

        if status_index == READ_INDEX_ERROR or len(ids_pool) == 0:
            return AsyncCrawlerResponse({},[status_index])


        ###### productcomment

        # (product_comments_container, status_comment) = await self.scrap_comment(ids_pool,keyword,\
        #                     page_nums,data_source,mode)
        (product_comments_container, status_comment) = await self.scrap_comment(ids_pool,kwargs)

        result_dict = {}
        result_dict['ids_pool'] = ids_pool
        result_dict['merged_search_index_df'] = merged_search_index_df
        result_dict['product_comments_container'] = product_comments_container
        my_return = AsyncCrawlerResponse(result_dict,[status_index,status_comment])


        return my_return

        # return (ids_pool,merged_search_index_df,product_comments_container,\
        #     [status_index,status_comment])



    async def process_index(self,kwargs:Dict[str,Any]) -> AsyncCrawlerResponse:
        """the entry function to be called by a workflow class for index mode"""

        ###### index
        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)

        result_dict = {}
        result_dict['ids_pool'] = ids_pool
        result_dict['merged_search_index_df'] = merged_search_index_df
        my_return = AsyncCrawlerResponse(result_dict,[status_index])

        return my_return #return (ids_pool,merged_search_index_df,[status_index])

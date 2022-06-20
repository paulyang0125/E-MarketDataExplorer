#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 20/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Async Crawler functionality.

Todo:\n
1. xxxxxx\n



"""
# shopee_data_explorer/shopee_crawler.py


from abc import ABC, abstractmethod
import asyncio
import os
import time
import logging
import aiohttp
import random
import nest_asyncio
nest_asyncio.apply()
import json
#import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
#from async_retrying import retry
from emarket_data_explorer import (SUCCESS,DATA_SOURCES,CSV_WRITE_ERROR,MODES)
import emarket_data_explorer


### logger
mylogger = logging.getLogger(__name__)
#mylogger.setLevel(logging.DEBUG)
#fh = logging.FileHandler('e-market.log')
fh = logging.FileHandler(f'{__name__}.log')
#fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)


class CrawlerHandler(ABC):
    """ test """

    def __init__(self, ip_addresses,proxy_auth):

        self.ip_addresses = ip_addresses
        self.proxy_auth = proxy_auth

    @abstractmethod
    def fetch(self,session, url, parsing_func):
        """ test """
        #pass

    @abstractmethod
    def rotate_ip(self):
        """
        This abstract method should return a list
        :rtype: list
        """
        #pass

    @abstractmethod
    async def download_all_sites(self,sites,parse_func):
        """ test """
        #pass


class ShopeeAsyncCrawlerHandler(CrawlerHandler):
    """ test """

    def __init__(self, ip_addresses,proxy_auth,header):
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
        self.parsing_candidates['parse_search_indexs'] = self.parse_search_indexs
        self.parsing_candidates['parse_good_info'] = self.parse_good_info
        self.parsing_candidates['parse_good_comments'] = self.parse_good_comments

        self.data_path = os.chdir(os.getcwd()) #will remove

    async def fetch(self, session, url, parsing_func):
        """ test """
        aio_proxies = self.rotate_ip()
        timeout = aiohttp.ClientTimeout(total=25)
        print("start fetching")
        tries = 0
        while tries < 3:
            print(f"proxy: {aio_proxies['http']}")
            try:
                #start = time.monotonic()
                async with session.get(url, headers=self.header,proxy=aio_proxies['http'],\
                    timeout=timeout,raise_for_status=True) as response:

                    if response.status == 200:
                        #print('each duration: ',time.monotonic() - start)
                        #print("Read {0} bytes from {1}".format(len(await response.read()), url))

                        text = await response.text()

                        parsed_result = parsing_func(text)

                        return parsed_result
                    else:
                        print("response.status: {response.status}")
                        tries += 1
                        aio_proxies = self.rotate_ip()

            except Exception as error:
                print('My Connection Error', str(error))
                if tries < 3:
                    aio_proxies = self.rotate_ip()
                else:
                    return

            tries += 1

    async def download_all_sites(self, sites, parse_func):
        """ test """
        async with aiohttp.ClientSession() as session:
            logging.info("Starting consumer")
            tasks = []

            for url in tqdm(sites,total=len(sites), position=0, leave=True):

                task = asyncio.ensure_future(self.fetch(session,url,parse_func))
                tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)

    def rotate_ip(self):
        """ test """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        return {
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}",
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}"}

    def parse_search_indexs(self,text):
        """ test """
        soup = BeautifulSoup(text, "lxml")
        getjson=json.loads(soup.text)
        print("parse_search_indexs succeeds")
        return getjson['items']

    def parse_good_info(self,text):
        """ test """
        processed_goods = text.replace("\\n","^n")
        processed_goods = processed_goods.replace("\\t","^t")
        processed_goods = processed_goods.replace("\\r","^r")
        goods_json = json.loads(processed_goods)
        print("parse_good_info succeeds")
        return goods_json

    def parse_good_comments(self,text):
        """ test """
        processed_comments_results= text.replace("\\n","^n")
        processed_comments_results=processed_comments_results.replace("\\t","^t")
        processed_comments_results=processed_comments_results.replace("\\r","^r")
        comments_json = json.loads(processed_comments_results)
        print("read_good_comments succeeds")
        return comments_json['comments']


    def read_search_indexs_url(self,keyword: str, page: int, page_length: int):
        """ test """
        page = page + 1
        url = 'https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword=' \
            + keyword + '&limit=' + str(page_length) + '&newest=' + str(page*page_length) + \
                '&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'
        return url

    def read_good_info_url(self,shop_id: int, item_id: int):
        """ test """
        url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(item_id) + '&shopid=' + \
                str(shop_id)
        return url

    def read_good_comments_url(self, shop_id: int, item_id: int):
        """ test """
        url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(item_id) + '&shop_id=' + \
            str(shop_id) + '&offset=0&limit=200&flag=1&filter=0'
        return url

    def process_raw_search_index(self, result:list) -> pd.DataFrame:
        """ test """
        product_items = {}
        #try:
        if not isinstance(result, NameError) and result:
            print(f"type: {type(result)}")
            for count, _ in enumerate(result):
                product_items[count] = result[count]['item_basic']

        #except NameError as ne:
        #    print('parsing exception:', str(ne))

        product_items=pd.DataFrame(product_items).T

        return product_items

    def split_list(self, alist, wanted_parts=1):
        """ test """
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    def clean_product_data(self):
        """ test """
        self.product_articles= []
        self.product_sku= []
        self.product_tags = []

    def extract_product_data(self, product:dict) -> None:
        """ test """
        try:
            if product['item']:
                if product['item']['description']:
                    self.product_articles.append(product['item']['description']\
                                                 .replace('\n', ' ').replace('\r', ''))
                else:
                    self.product_articles.append('na')
                if product['item']['models']:
                    # bug, to remove /n and /r from list of dict of value
                    #i for i in product['item']['models']
                    self.product_sku.append(product['item']['models'])
                    #self.product_sku.append(product['item']['models']\
                    #                        .replace('\n', ' ').replace('\r', ''))
                else:
                    self.product_sku.append('na')
                if product['item']['hashtag_list']:
                    self.product_tags.append(product['item']['hashtag_list'])
                    #self.product_tags.append(product['item']['hashtag_list']\
                    #                         .replace('\n', ' ').replace('\r', ''))
                else:
                    self.product_sku.append('na')


        except KeyError as error:
            print('I got a KeyError - reason "%s"' % str(error))
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')
        except TypeError as error:
            print('I got a TypeError - reason "%s"' % str(error))
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')


    def aggregate_product_data(self, product_items_container: pd.DataFrame, \
        product_items: pd.DataFrame) -> pd.DataFrame:
        """ test """

        #for debug
        #global debug_list_1
        #global debug_list_2
        #debug_list_1 = self.product_sku
        #debug_list_2 = self.product_tags

        product_items['articles'] = pd.Series(self.product_articles)
        product_items['SKU'] = pd.Series(self.product_sku)
        product_items['hashtag_list'] = pd.Series(self.product_tags)
        product_items_container = pd.concat([product_items_container,product_items],\
            axis=0)
        return product_items_container

    def write_csv(self, product_container:pd.DataFrame,my_keyword:str, \
        data_source: int,crawler_mode: str) -> int:
        """write the scrapped data stored in dataframe into CSV"""
        try:
            source = DATA_SOURCES[data_source]
            file_name = f'{source}_{my_keyword}_{crawler_mode}.csv'
            #product_container = product_container.replace(r'\r+|\n+|\t+','', regex=True)
            #product_container.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
            product_container.to_csv(file_name,encoding = 'utf-8-sig')
            print(f"the container has wrote into {file_name} in {self.data_path}")
            #os.chdir(self.owd)
            return SUCCESS
        except OSError:  # Catch file IO problems
            #os.chdir(self.owd)
            return CSV_WRITE_ERROR

    def update_comment_data(self, comment) -> pd.DataFrame:
        """ test """
        #mydebug_list.append(comment)
        if not comment:
            user_comment = pd.DataFrame()
        else:
            user_comment = pd.DataFrame(comment) #covert comment to data frame
        #mydebug_list.append(user_comment)

        if not user_comment.empty:
            models=[]
            for item in user_comment['product_items']:
                if pd.DataFrame(item).filter(regex = 'model_name').shape[1] != 0:
                    models.append(pd.DataFrame(item)['model_name'].tolist())
                else:
                    mylogger.warning('No model_name')
                    models.append(None)

            user_comment['product_items']= models # puts models aka SKUs in

        self.product_comments_container = pd.concat([self.product_comments_container,\
             user_comment],axis= 0)
        #mydebug_list.append(self.product_comments_container)
        # debug
        #print("process_comment_data->comment_container:head", product_comments_container.head(5))
        #print("process_comment_data->comment_container:tail", product_comments_container.tail(5))

        return self.product_comments_container

    async def scrap_index(self,keyword,page_nums,page_length,data_source,mode):
        """ test """
        print("Crawler Setup started")
        #page_num = num_of_product // page_length
        print("Main started")

        ###### index

        read_search_indexs_urls = [self.read_search_indexs_url(keyword,page,page_length) for page \
             in range(page_nums)]
        search_index_results = await asyncio.gather(self.download_all_sites(\
            read_search_indexs_urls,self.parsing_candidates['parse_search_indexs']))

        print(f"how many index: {len(search_index_results[0])}")

        ### start parsing
        #ids_pool = []
        processed_index_dfs = [self.process_raw_search_index(each) for each in \
            search_index_results[0] if search_index_results[0]]
        merged_search_index_df = pd.concat(processed_index_dfs)
        merged_search_index_df = merged_search_index_df.drop_duplicates(subset=['itemid'])

        self.ids_pool.append([(item_id, shop_id, name) for \
            item_id, shop_id, name in zip(merged_search_index_df['itemid'].tolist(),\
                        merged_search_index_df['shopid'].tolist(),\
                                merged_search_index_df['name'].tolist())])
         #shopee,will remove
        if mode == emarket_data_explorer.ALL:
            crawler_mode = MODES[mode].split(':')[2]
        else:
            crawler_mode = MODES[mode]

        ### write data
        print('start writing - product')
        self.write_csv(merged_search_index_df,keyword,data_source,crawler_mode)

        return merged_search_index_df, self.ids_pool, SUCCESS

    async def scrap_comment(self,ids_pool,keyword,page_nums,data_source,mode):
        """ test """
        ## create urls
        search_comments_urls = []
        for pages in ids_pool:
            for item in pages: # item is tutle
                search_comments_urls.append(self.read_good_comments_url(item[1],item[0]))

        ## start crawler
        print('start crawler - comment')
        comments_list = []
        sites_lists = self.split_list(search_comments_urls, wanted_parts=page_nums)
        for sites in sites_lists:
            the_comment_results = await asyncio.gather(self.download_all_sites(sites,\
                            self.parsing_candidates['parse_good_comments']))
            comments_list.append(the_comment_results)

        print(f"how many good comment: {len(comments_list)}")

        ### start parsing
        print('start parsing - comment ')
        #my_list3[0][0][0],[0]
        for each_loop in comments_list:
            for each_product in each_loop[0]:
                product_comments_container = self.update_comment_data(each_product)

        if mode == emarket_data_explorer.ALL:
            crawler_mode = MODES[mode].split(':')[1]
        else:
            crawler_mode = MODES[mode]

        #crawler_mode = get_crawler_mode(mode)

        ### write data
        print('start writing - comment ')
        self.write_csv(product_comments_container,keyword,data_source,crawler_mode)

        return (product_comments_container , SUCCESS)

    async def scrap_product_info(self,ids_pool,merged_search_index_df,page_nums,\
        keyword,data_source, mode):
        """ test """
         ## create urls
        search_results_urls =[]
        for pages in ids_pool:
            for item in pages: # item is tutle \
                #print(item[0],item[1],item[2]) #'itemid', 'shopid', 'name'
                search_results_urls.append(self.read_good_info_url(item[1],item[0]))

        ## start crawler
        product_list = []
        print('start crawler - product')
        #
        sites_lists = self.split_list(search_results_urls, wanted_parts=page_nums)
        for sites in sites_lists:
            the_product_results = await asyncio.gather(self.download_all_sites(sites,\
                                    self.parsing_candidates['parse_good_info']))
            product_list.append(the_product_results)

        print(f"how many good info: {len(product_list)}")


        ### start parsing
        print('start parsing - product')
        #my_list2[0][0][0]['item']
        for each_loop in product_list:
            for each_page in each_loop[0]:
                self.extract_product_data(each_page)

        self.product_items_container = self.aggregate_product_data(self.\
            product_items_container,merged_search_index_df)

        self.clean_product_data()

        if mode == emarket_data_explorer.ALL:
            crawler_mode = MODES[mode].split(':')[0]
        else:
            crawler_mode = MODES[mode]


        ### write data
        print('start writing - product')
        self.write_csv(self.product_items_container,keyword,data_source,crawler_mode)

        return (self.product_comments_container, SUCCESS)

    def get_page(self,num_of_product,page_length):
        """ test """
        page_nums = num_of_product // page_length
        return page_nums

    async def process_all(self,keyword,num_of_product,page_length,data_source,mode):
        """ test """
        ###### index
        page_nums = self.get_page(num_of_product,page_length)
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(
                        keyword,page_nums,page_length,data_source,mode)

        ###### productinfo

        (product_comments_container, status_product) = await self.scrap_product_info(ids_pool,\
                        merged_search_index_df,page_nums,keyword,data_source,mode)

        ###### productcomment

        (product_comments_container, status_comment) = await self.scrap_comment(ids_pool,keyword,\
                        page_nums,data_source,mode)

        return (ids_pool,[status_index,status_product,status_comment])

    async def process_product(self,keyword,num_of_product,page_length,data_source,mode):
        """ test """
        ###### index

        page_nums = self.get_page(num_of_product,page_length)
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(
                    keyword,page_nums,page_length,data_source,mode)

        ###### productinfo

        (product_comments_container, status_product) = await self.scrap_product_info(ids_pool,\
                    merged_search_index_df,page_nums,keyword,data_source,mode)

        return (ids_pool,[status_index,status_product])


    async def process_comment(self,keyword,num_of_product,page_length,data_source,mode):
        """ test """

        ###### index

        page_nums = self.get_page(num_of_product,page_length)
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(
                            keyword,page_nums,page_length,data_source,mode)

        ###### productcomment

        (product_comments_container, status_comment) = await self.scrap_comment(ids_pool,keyword,\
                            page_nums,data_source,mode)

        return (ids_pool,[status_index,status_comment])


    async def process_index(self,keyword,num_of_product,page_length,data_source,mode):
        """test"""

        ###### index

        page_nums = self.get_page(num_of_product,page_length)
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(
                    keyword,page_nums,page_length,data_source,mode)

        return (ids_pool,[status_index])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 20/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Async Crawler functionality.

Todo:\n
x 1. tqdm is not working well for async version \n
x 2. errors are not used well in async version \n
x 3. need to define the datatype for this \n



"""
# shopee_data_explorer/shopee_async_crawler.py

import asyncio
import os
import time
import logging
import aiohttp
import random
#import nest_asyncio
#nest_asyncio.apply()
#import tqdm.asyncio
import pandas as pd
from tqdm import tqdm
#from async_retrying import retry
from emarket_data_explorer.classtype import CrawlerHandler
import emarket_data_explorer
from emarket_data_explorer import (MODES, READ_INDEX_ERROR,\
    CSV_WRITE_ERROR,DATA_FOLDER_WRITE_ERROR,READ_PRODUCT_ERROR, READ_COMMENT_ERROR,SUCCESS)
from emarket_data_explorer.datatype import AsyncCrawlerResponse

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


# class CrawlerHandler(ABC):
#     """ test """

#     def __init__(self, ip_addresses,proxy_auth):

#         self.ip_addresses = ip_addresses
#         self.proxy_auth = proxy_auth

#     @abstractmethod
#     def fetch(self,session, url, parsing_func):
#         """ test """
#         #pass

#     @abstractmethod
#     def rotate_ip(self):
#         """
#         This abstract method should return a list
#         :rtype: list
#         """
#         #pass

#     @abstractmethod
#     async def download_all_sites(self,sites,parse_func):
#         """ test """
#         #pass


class ShopeeAsyncCrawlerHandler(CrawlerHandler):
    """ test """

    def __init__(self, ip_addresses,proxy_auth,header, data_handler):
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

    async def _fetch(self, session, url, parsing_func):
        """ test """

        aio_proxies = self._rotate_ip()
        timeout = aiohttp.ClientTimeout(total=25)
        mylogger.debug("start fetching")
        tries = 0

        while tries < 3:
            mylogger.debug(f"proxy: {aio_proxies['http']}")
            try:
                start = time.monotonic()
                async with session.get(url, headers=self.header,proxy=aio_proxies['http'],\
                    timeout=timeout,raise_for_status=True) as response:
                    # target = url.rpartition('/')[-1]
                    # size = int(response.headers.get('content-length', 0)) or None
                    # position = await progress_queue.get()
                    # progressbar = tqdm(
                    #     desc=target, total=size, leave=False,
                    # )



                    if response.status == 200:
                        mylogger.debug('each duration: %d',time.monotonic() - start)
                        mylogger.debug("Read {0} bytes from {1}".format(len(await response.read()), url))

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

    async def _download_all_sites(self, sites, parse_func):
        """ test """
        results = []
        async with aiohttp.ClientSession() as session:
            logging.info("Starting to create the session")
            tasks = []

            #progress_queue = asyncio.Queue(loop=loop)
            #for pos in range(5):
            #    progress_queue.put_nowait(pos)
            #for url in tqdm(sites,total=len(sites), position=0, leave=True):
            for url in sites:
            #for url in tqdm.asyncio(sites,total=len(sites), position=0, leave=True):
                task = asyncio.ensure_future(self._fetch(session,url,parse_func))
                tasks.append(task)
            #pbar = tqdm(total=len(task), position=0, ncols=90)

            for future in tqdm(asyncio.as_completed(tasks),\
                total=len(sites), position=0, leave=True, desc="scrap content"):
                result = await future
                results.append(result)

            #return await asyncio.gather(*tasks, return_exceptions=True)
            return results

    def _rotate_ip(self):
        """ test """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        return {
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}",
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}"}

    # def parse_search_indexs(self,text):
    #     """ test """
    #     soup = BeautifulSoup(text, "lxml")
    #     getjson=json.loads(soup.text)
    #     print("parse_search_indexs succeeds")
    #     return getjson['items']

    # def parse_good_info(self,text):
    #     """ test """
    #     processed_goods = text.replace("\\n","^n")
    #     processed_goods = processed_goods.replace("\\t","^t")
    #     processed_goods = processed_goods.replace("\\r","^r")
    #     goods_json = json.loads(processed_goods)
    #     print("parse_good_info succeeds")
    #     return goods_json

    # def parse_good_comments(self,text):
    #     """ test """
    #     processed_comments_results= text.replace("\\n","^n")
    #     processed_comments_results=processed_comments_results.replace("\\t","^t")
    #     processed_comments_results=processed_comments_results.replace("\\r","^r")
    #     comments_json = json.loads(processed_comments_results)
    #     print("read_good_comments succeeds")
    #     return comments_json['comments']


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

    # def process_raw_search_index(self, result:list) -> pd.DataFrame:
    #     """ test """
    #     product_items = {}
    #     #try:
    #     if not isinstance(result, NameError) and result:
    #         print(f"type: {type(result)}")
    #         for count, _ in enumerate(result):
    #             product_items[count] = result[count]['item_basic']

    #     #except NameError as ne:
    #     #    print('parsing exception:', str(ne))

    #     product_items=pd.DataFrame(product_items).T

    #     return product_items

    def split_list(self, alist, wanted_parts=1):
        """ test """
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    # def clean_product_data(self):
    #     """ test """
    #     self.product_articles= []
    #     self.product_sku= []
    #     self.product_tags = []

    # def extract_product_data(self, product:dict) -> None:
    #     """ test """
    #     try:
    #         if product['item']:
    #             if product['item']['description']:
    #                 self.product_articles.append(product['item']['description']\
    #                                              .replace('\n', ' ').replace('\r', ''))
    #             else:
    #                 self.product_articles.append('na')
    #             if product['item']['models']:
    #                 # bug, to remove /n and /r from list of dict of value
    #                 #i for i in product['item']['models']
    #                 self.product_sku.append(product['item']['models'])
    #                 #self.product_sku.append(product['item']['models']\
    #                 #                        .replace('\n', ' ').replace('\r', ''))
    #             else:
    #                 self.product_sku.append('na')
    #             if product['item']['hashtag_list']:
    #                 self.product_tags.append(product['item']['hashtag_list'])
    #                 #self.product_tags.append(product['item']['hashtag_list']\
    #                 #                         .replace('\n', ' ').replace('\r', ''))
    #             else:
    #                 self.product_sku.append('na')


    #     except KeyError as error:
    #         print('I got a KeyError - reason "%s"' % str(error))
    #         self.product_articles.append('na')
    #         self.product_sku.append('na')
    #         self.product_tags.append('na')
    #     except TypeError as error:
    #         print('I got a TypeError - reason "%s"' % str(error))
    #         self.product_articles.append('na')
    #         self.product_sku.append('na')
    #         self.product_tags.append('na')


    # def aggregate_product_data(self, product_items_container: pd.DataFrame, \
    #     product_items: pd.DataFrame) -> pd.DataFrame:
    #     """ test """

    #     #for debug
    #     #global debug_list_1
    #     #global debug_list_2
    #     #debug_list_1 = self.product_sku
    #     #debug_list_2 = self.product_tags

    #     product_items['articles'] = pd.Series(self.product_articles)
    #     product_items['SKU'] = pd.Series(self.product_sku)
    #     product_items['hashtag_list'] = pd.Series(self.product_tags)
    #     product_items_container = pd.concat([product_items_container,product_items],\
    #         axis=0)
    #     return product_items_container

    # def write_csv(self, product_container:pd.DataFrame,my_keyword:str, \
    #     data_source: int,crawler_mode: str) -> int:
    #     """write the scrapped data stored in dataframe into CSV"""
    #     try:
    #         source = DATA_SOURCES[data_source]
    #         file_name = f'{source}_{my_keyword}_{crawler_mode}.csv'
    #         #product_container = product_container.replace(r'\r+|\n+|\t+','', regex=True)
    #         #product_container.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
    #         product_container.to_csv(file_name,encoding = 'utf-8-sig')
    #         print(f"the container has wrote into {file_name} in {self.data_path}")
    #         #os.chdir(self.owd)
    #         return SUCCESS
    #     except OSError:  # Catch file IO problems
    #         #os.chdir(self.owd)
    #         return CSV_WRITE_ERROR

    # def update_comment_data(self, comment) -> pd.DataFrame:
    #     """ test """
    #     #mydebug_list.append(comment)
    #     if not comment:
    #         user_comment = pd.DataFrame()
    #     else:
    #         user_comment = pd.DataFrame(comment) #covert comment to data frame
    #     #mydebug_list.append(user_comment)

    #     if not user_comment.empty:
    #         models=[]
    #         for item in user_comment['product_items']:
    #             if pd.DataFrame(item).filter(regex = 'model_name').shape[1] != 0:
    #                 models.append(pd.DataFrame(item)['model_name'].tolist())
    #             else:
    #                 mylogger.warning('No model_name')
    #                 models.append(None)

    #         user_comment['product_items']= models # puts models aka SKUs in

    #     self.product_comments_container = pd.concat([self.product_comments_container,\
    #          user_comment],axis= 0)
    #     #mydebug_list.append(self.product_comments_container)
    #     # debug
    #     #print("process_comment_data->comment_container:head", product_comments_container.head(5))
    #     #print("process_comment_data->comment_container:tail", product_comments_container.tail(5))

    #     return self.product_comments_container

    #async def scrap_index(self,keyword,page_nums,page_length,data_source,mode):
    async def scrap_index(self,kwargs):
        """ test """
        mylogger.info("scrap_index starts")
        #page_num = num_of_product // page_length


        ###### index

        # read_search_indexs_urls = [self.read_search_indexs_url(keyword,page,page_length) for page \
        #      in range(page_nums)]

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

        mylogger.debug(f"how many index: {len(search_index_results[0])}")

        ### start parsing
        #ids_pool = []
        # processed_index_dfs = [self.process_raw_search_index(each) for each in \
        #     search_index_results[0] if search_index_results[0]]

        # processed_index_dfs = [self.process_raw_search_index(each) for each in \
        #     search_index_results[0] if search_index_results[0]]

        processed_index_dfs = [kwargs['data_processor'].process_raw_search_index(each) for each in \
            search_index_results[0] if search_index_results[0]]

        merged_search_index_df = pd.concat(processed_index_dfs)
        merged_search_index_df = merged_search_index_df.drop_duplicates(subset=['itemid'])

        self.ids_pool.append([(item_id, shop_id, name) for \
            item_id, shop_id, name in zip(merged_search_index_df['itemid'].tolist(),\
                        merged_search_index_df['shopid'].tolist(),\
                                merged_search_index_df['name'].tolist())])
        #shopee,will remove
        # if mode == emarket_data_explorer.ALL:
        #     crawler_mode = MODES[mode].split(':')[2]
        # else:
        #     crawler_mode = MODES[mode]

        if kwargs['mode'] == emarket_data_explorer.ALL:
            crawler_mode = MODES[kwargs['mode']].split(':')[2]
        else:
            crawler_mode = MODES[kwargs['mode']]

        mylogger.debug(f"index.crawler_mode: {crawler_mode} ")
        ### write data
        mylogger.info('start writing - product')
        #self.write_csv(merged_search_index_df,keyword,data_source,crawler_mode)
        write_csv_status = kwargs['database'].write_csv(merged_search_index_df,kwargs['keyword'],\
           kwargs['data_source'],crawler_mode)

        # if write_csv_status != SUCCESS:
        #     return merged_search_index_df, self.ids_pool, write_csv_status

        return merged_search_index_df, self.ids_pool, write_csv_status

    #async def scrap_comment(self,ids_pool,keyword,page_nums,data_source,mode):
    async def scrap_comment(self,ids_pool,kwargs):
        """ test """
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

        mylogger.debug(f"how many good comment: {len(comments_list)}")

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

        # if mode == emarket_data_explorer.ALL:
        #     crawler_mode = MODES[mode].split(':')[1]
        # else:
        #     crawler_mode = MODES[mode]

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

    # async def scrap_product_info(self,ids_pool,merged_search_index_df,page_nums,\
    #     keyword,data_source, mode):
    async def scrap_product_info(self,ids_pool,merged_search_index_df,kwargs):
        """ test """
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
        #
        # sites_lists = self.split_list(search_results_urls, wanted_parts=page_nums)
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


        # self.product_items_container = self.aggregate_product_data(self.\
        #     product_items_container,merged_search_index_df)
        self.product_items_container = kwargs['data_processor'].aggregate_product_data(self.\
            product_items_container,merged_search_index_df)

        #self.clean_product_data()
        kwargs['data_processor'].clean_product_data()

        # if mode == emarket_data_explorer.ALL:
        #     crawler_mode = MODES[mode].split(':')[0]
        # else:
        #     crawler_mode = MODES[mode]

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

    def get_page(self,num_of_product,page_length):
        """ test """
        page_nums = num_of_product // page_length
        return page_nums

    # async def process_all(self,keyword,num_of_product,page_length,data_source,mode,\
    #     data_handler, db_handler):
    async def process_all(self,kwargs):
        """ test """
        ###### index
        # page_nums = self.get_page(num_of_product,page_length)
        # merged_search_index_df, ids_pool, status_index = await self.scrap_index(
        #                 keyword,page_nums,page_length,data_source,mode)

        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)

        if status_index == READ_INDEX_ERROR or len(ids_pool) == 0:
             #my_return = AsyncCrawlerResponse({},[status_index])
             return AsyncCrawlerResponse({},[status_index])

        ###### productinfo

        # (product_items_container, status_product) = await self.scrap_product_info(ids_pool,\
        #                 merged_search_index_df,page_nums,keyword,data_source,mode)
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
    async def process_product(self,kwargs):
        """ test """
        ###### index

        # page_nums = self.get_page(num_of_product,page_length)
        # merged_search_index_df, ids_pool, status_index = await self.scrap_index(
        #             keyword,page_nums,page_length,data_source,mode)

        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)
        if status_index == READ_INDEX_ERROR or len(ids_pool) == 0:
             return AsyncCrawlerResponse({},[status_index])

        ###### productinfo

        # (product_items_container, status_product) = await self.scrap_product_info(ids_pool,\
        #             merged_search_index_df,page_nums,keyword,data_source,mode)
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


    #async def process_comment(self,keyword,num_of_product,page_length,data_source,mode):
    async def process_comment(self,kwargs):
        """ test """

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

        return (ids_pool,merged_search_index_df,product_comments_container,\
            [status_index,status_comment])


    #async def process_index(self,keyword,num_of_product,page_length,data_source,mode):
    async def process_index(self,kwargs):
        """test"""

        ###### index

        # page_nums = self.get_page(num_of_product,page_length)
        # merged_search_index_df, ids_pool, status_index = await self.scrap_index(
        #             keyword,page_nums,page_length,data_source,mode)

        page_nums = self.get_page(kwargs['num_of_product'],kwargs['page_length'])
        kwargs['page_nums'] = page_nums
        merged_search_index_df, ids_pool, status_index = await self.scrap_index(kwargs)

        result_dict = {}
        result_dict['ids_pool'] = ids_pool
        result_dict['merged_search_index_df'] = merged_search_index_df
        my_return = AsyncCrawlerResponse(result_dict,[status_index])


        #return (ids_pool,merged_search_index_df,[status_index])
        return my_return

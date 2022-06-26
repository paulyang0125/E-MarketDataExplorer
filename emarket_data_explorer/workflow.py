#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the workflow functionality.

Todo:\n


"""
# shopee_data_explorer/workflow.py

from abc import ABC
from typing import Dict, List, Any, Tuple
import asyncio
import time


##workflow

class WorkFlow(ABC):
    """the abstract class of workflow"""
    #pass

class ShopeeAsyncWorkFlow(WorkFlow):
    """ the implementation of workflow for shopee async io"""

    def do_workflow_all(self,**kwargs:Dict[str,Any]) -> Tuple[Dict[str,Any], List[int]]:
    #def do_workflow_all(self,keyword,num_of_product,\
    # page_length,data_source,ip_addresses,proxy_auth,header):
        """ workflow for all """

        #kwargs['ip_addresses']

        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        # result = asyncio.run(kwargs['handler'].process_all(kwargs['keyword'], \
        #     kwargs['num_of_product'],kwargs['page_length'], kwargs['data_source'],
        #     kwargs['mode'], kwargs['data_processor'],kwargs['database']),debug=True)

        #result = asyncio.run(kwargs['handler'].process_all(kwargs),debug=True)
        read = asyncio.run(kwargs['handler'].process_all(kwargs),debug=True)



        #asyncio.run(shopee_handler.process_all(keyword, num_of_product,\
        # page_length, data_source),debug=True)

        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        # scraper_response = {
        #     "ids_pool":result[0],
        #     "obtained_index_num":len(result[1].index),
        #     "obtained_good_num":len(result[2].index),
        #     "obtained_comment_num":len(result[3].index),
        # }

        scraper_response = {
            "ids_pool":read.results['ids_pool'],
            "obtained_index_num":len(read.results['merged_search_index_df'].index),
            "obtained_good_num":len(read.results['product_items_container'].index),
            "obtained_comment_num":len(read.results['product_comments_container'].index),
        }

        #return (scraper_response, result[4])
        return (scraper_response, read.errors)

        #return result

        # return (ids_pool,merged_search_index_df,product_comments_container,\
        #     product_comments_container,[status_index,status_product,status_comment])

        # if not product_items_container.empty and not product_comments_container.empty:
        # scraper_response = {
        # "keyword":keyword,
        # "page_num": page_num,
        # "page_length":page_length,
        # "obtained_product_num":len(product_items_container.index),
        # "obtained_comment_num":len(product_comments_container.index),
        # }

        # return ScrapingInfo(scraper_response, read.error)






    def do_workflow_product_info(self,**kwargs:Dict[str,Any]) -> Tuple[Dict[str,Any], List[int]]:
        """ workflow for product info """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        # result = asyncio.run(kwargs['handler'].process_product(kwargs['keyword'],\
        #     kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
        #         kwargs['mode'],kwargs['data_processor'],kwargs['database']),debug=True)
        #result = asyncio.run(kwargs['handler'].process_product(kwargs),debug=True)
        read = asyncio.run(kwargs['handler'].process_product(kwargs),debug=True)
        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        scraper_response = {
            "ids_pool":read.results['ids_pool'],
            "obtained_index_num":len(read.results['merged_search_index_df'].index),
            "obtained_good_num":len(read.results['product_items_container'].index),

        }

        #return (scraper_response, result[4])
        return (scraper_response, read.errors)

        # scraper_response = {
        #     "ids_pool":result[0],
        #     "obtained_index_num":len(result[1].index),
        #     "obtained_good_num":len(result[2].index),

        # }
        # return (scraper_response, result[3])

    def do_workflow_product_comment(self,**kwargs:Dict[str,Any]) -> Tuple[Dict[str,Any], List[int]]:
        """ workflow for comment """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])
        # result = asyncio.run(kwargs['handler'].process_comment(kwargs['keyword'],\
        #     kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
        #         kwargs['mode'],kwargs['data_processor'],kwargs['database']),debug=True)

        #result = asyncio.run(kwargs['handler'].process_comment(kwargs),debug=True)
        read = asyncio.run(kwargs['handler'].process_comment(kwargs),debug=True)

        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        scraper_response = {
            "ids_pool":read.results['ids_pool'],
            "obtained_index_num":len(read.results['merged_search_index_df'].index),
            "obtained_comment_num":len(read.results['product_comments_container'].index),
        }

        #return (scraper_response, result[4])
        return (scraper_response, read.errors)

        # scraper_response = {
        #     "ids_pool":result[0],
        #     "obtained_index_num":len(result[1].index),
        #     "obtained_comment_num":len(result[2].index),
        # }

        # return (scraper_response, result[3])


        #return result

    def do_workflow_product_index(self,**kwargs:Dict[str,Any]) -> Tuple[Dict[str,Any], List[int]]:
        """ workflow for the index """
        start_time = time.time()
        #shopee_handler = ShopeeAsyncCrawlerHandler(ip_addresses=kwargs['ip_addresses'],\
        #    proxy_auth=kwargs['proxy_auth'],header=kwargs['header'])

        # result = asyncio.run(kwargs['handler'].process_index(kwargs['keyword'],\
        #     kwargs['num_of_product'], kwargs['page_length'], kwargs['data_source'],\
        #         kwargs['mode'],kwargs['data_processor'],kwargs['database']),debug=True)

        #result = asyncio.run(kwargs['handler'].process_index(kwargs),debug=True)
        read = asyncio.run(kwargs['handler'].process_index(kwargs),debug=True)

        #shopee_handler = ShopeeAsycCrawlerHandler(ip_addresses=ip_addresses,\
        # proxy_auth=proxy_auth,header=header)
        #merged_search_index_df, ids_pool, status = asyncio.run(shopee_handler.\

        duration = time.time() - start_time
        print(f"Duration {duration} seconds")

        scraper_response = {
            "ids_pool":read.results['ids_pool'],
            "obtained_index_num":len(read.results['merged_search_index_df'].index),
        }

        return (scraper_response, read.errors)

        # scraper_response = {
        #     "ids_pool":result[0],
        #     "obtained_index_num":len(result[1].index),
        # }

        # return (scraper_response, result[2])

        #return result

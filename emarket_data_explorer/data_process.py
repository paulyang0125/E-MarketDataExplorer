#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data process functionality.

Todo:\n
1. when do parallel in v1.4, this aggregation shouldn't work
so need a new way to aggregate later\n



"""
# shopee_data_explorer/data_process.py


import logging
from typing import Any, Dict, List
import json
import pandas as pd
from bs4 import BeautifulSoup



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


### remove ###

### remove ###

class ShopeeAsyncCrawlerDataProcesser:
    """This class provides the data process functionality for async version"""

    def __init__(self, data_source:str) -> None:
        self.data_source = data_source
        #self.product_items = []
        self.product_articles = []
        self.product_sku = []
        self.product_tags = []
        #self.product_items_container = pd.DataFrame()
        self.product_comments_container = pd.DataFrame()

    def parse_search_indexs(self,text:str) -> List[Dict[str, Any]]:
        """ parse the scarped index data by transferring to json """

        soup = BeautifulSoup(text, "lxml")
        getjson=json.loads(soup.text)
        mylogger.debug("parse_search_indexs succeeds")
        return getjson['items']

    def parse_good_info(self,text:str) -> List[Dict[str, Any]]:
        """ parse the scarped index data by transferring to json """

        processed_goods = text.replace("\\n","^n")
        processed_goods = processed_goods.replace("\\t","^t")
        processed_goods = processed_goods.replace("\\r","^r")
        goods_json = json.loads(processed_goods)
        mylogger.debug("parse_good_info succeeds")
        return goods_json

    def parse_good_comments(self,text:str) -> List[Dict[str, Any]]:
        """ parse the scarped comment data by transferring to json """

        processed_comments_results= text.replace("\\n","^n")
        processed_comments_results=processed_comments_results.replace("\\t","^t")
        processed_comments_results=processed_comments_results.replace("\\r","^r")
        comments_json = json.loads(processed_comments_results)
        mylogger.debug("read_good_comments succeeds")
        return comments_json['comments']


    def process_raw_search_index(self, result:List[Dict[str, Any]]) -> pd.DataFrame:
        """process the raw shopee search data from its api

            Args:
                result:List[[Dict[str, Any]]]: raw data scrapped from shopee\n

            Returns:
                product_items (pd.DataFrame): search index data

        """
        product_items = {}
        #try:
        if not isinstance(result, NameError) and result:
            mylogger.debug("type: %s" , str(type(result)))
            for count, _ in enumerate(result):
                product_items[count] = result[count]['item_basic']

        #except NameError as ne:
        #    print('parsing exception:', str(ne))

        product_items=pd.DataFrame(product_items).T

        return product_items

    def clean_product_data(self) -> None:
        """ clean the three list of collecting product detail """
        self.product_articles= []
        self.product_sku= []
        self.product_tags = []

    def extract_product_data(self, product:Dict[str,Any]) -> None:
        """ extract 'description', 'models' and 'hashtag_list' and append them into lists
           for later pd concatenation

        """
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
            mylogger.warning('I got a KeyError - reason %s', str(error))
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')
        except TypeError as error:
            mylogger.warning('I got a TypeError - reason %s',  str(error))
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')


    def aggregate_product_data(self, product_items_container: pd.DataFrame, \
        product_items: pd.DataFrame) -> pd.DataFrame:
        """ it accumulates three items for a page and then aggregate into a df """

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

    def update_comment_data(self, comment:List[Dict[str, Any]]) -> pd.DataFrame:
        """ extract 'model_name' from the column of 'product_items' and then just replace
           'product_items' with the extraction and then concat with the comment container

        """
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
        #mylogger.debug("process_comment_data->comment_container:head", product_comments_container.head(5))
        #mylogger.debug("process_comment_data->comment_container:tail", product_comments_container.tail(5))

        return self.product_comments_container

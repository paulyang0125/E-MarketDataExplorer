#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data process functionality.

Todo:\n
1. when do parallel in v1.3, this aggregation shouldn't work
   so need a new way to aggregate later\n



"""
# shopee_data_explorer/data_process.py


import logging
from typing import Any, Dict, List
import pandas as pd



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



class CrawlerDataProcesser:
    """This class provides the data process functionality.

    Args:
        data_source (str): this indicate which e-commerce site you want to scrap such as
        shopee, ptt or amazon.


    """

    def __init__(self, data_source:str) -> None:
        self.data_source = data_source
        self.product_items = []
        self.product_articles = []
        self.product_sku = []
        self.product_tags = []

    def process_product_data(self,product:Dict[str, Any]) -> None:
        """extract 'description', 'models' and 'hashtag_list' and append them into lists
           for later pd concatenation

            Args:
                product (Dict[str, Any] or JSON): the product detail scrapped from shopee

            Returns:
                None
        """
        if product:
            self.product_articles.append(product['description'])
            self.product_sku.append(product['models'])
            self.product_tags.append(product['hashtag_list'])
        else:
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')



    def clean_product_data(self):
        """clean the three list of collecting product detail.
        this app designs to collect one round and then save them immediately
        (round depends page length ex.50)

            Args:
                None

            Returns:
                None

        """
        self.product_articles= []
        self.product_sku= []
        self.product_tags = []

    def write_shopee_goods_data(self,product_items_container:pd.DataFrame, my_keyword:str):
        """UNUSED, it writes data to csv by dataframe built-in function to_csv()

            Args:
                product_items_container (pd.DataFrame): the concat product detail scrapped
                from shopee\n
                my_keyword (str) : user's keyword entered into the command line

            Returns:
                None

        """
        product_items_container.to_csv(self.data_source + "_" + my_keyword +'_goods_data.csv',\
             encoding = 'utf-8-sig')

    def write_shopee_comments_data(self,product_comments_container:pd.DataFrame,my_keyword:str):
        """UNUSED, it writes data to csv by dataframe built-in function to_csv()

            Args:
                product_items_container (pd.DataFrame): the concat product comment scrapped
                from shopee\n
                my_keyword (str) : user's keyword entered into the command line

            Returns:
                None
        """
        product_comments_container.to_csv(self.data_source + "_" + my_keyword + \
            '_comments_data.csv', encoding = 'utf-8-sig')

    def process_comment_data(self,comment:List[Dict[str, Any]], product_comments_container:\
        pd.DataFrame) -> pd.DataFrame:
        """extract 'model_name' from the column of 'product_items' and then just replace
           'product_items' with the extraction and then concat with the comment container

            Args:
                comment (JSON): the comment data scraped from shopee\n
                product_comment_container (pd.DataFrame): the concat product
                comment dataframe

            Returns:
                product_comments_container (pd.DataFrame)

        """
        user_comment = pd.DataFrame(comment) #covert comment to data frame
        if not user_comment.empty:
            models=[]
            for item in user_comment['product_items']:
                if pd.DataFrame(item).filter(regex = 'model_name').shape[1] != 0:
                    models.append(pd.DataFrame(item)['model_name'].tolist())
                else:
                    mylogger.warning('No model_name')
                    models.append(None)

            user_comment['product_items']= models # puts models aka SKUs in

        #todo: when do parallel in v1.3, this aggregation shouldn't work
        #so need a new way to aggregate later
        product_comments_container = pd.concat([product_comments_container, user_comment], \
            axis= 0)
        # debug
        #print("process_comment_data->comment_container:head", product_comments_container.head(5))
        #print("process_comment_data->comment_container:tail", product_comments_container.tail(5))

        return product_comments_container



    def aggregate_product_data(self, product_items_container: pd.DataFrame, product_items: \
        pd.DataFrame) -> pd.DataFrame:
        """it accumulate three items for a page and then aggregate

            Args:
                product_items (pd.DataFrame): the search index data scraped from shopee.\n
                product_item_container (pd.DataFrame): the concat product container.

            Returns:
                product_items_container (pd.DataFrame)

        """
        product_items['articles'] = pd.Series(self.product_articles)
        product_items['SKU'] = pd.Series(self.product_sku)
        product_items['hashtag_list'] = pd.Series(self.product_tags)
        # debug
        #print("aggregate_product_data->product-item:head", product_items.head(5))
        #print("aggregate_product_data->product-item:tail", product_items.tail(5))
        product_items_container = pd.concat([product_items_container,product_items],\
            axis=0)
        # debug
        #print("aggregate_product_data->container:head", product_items_container.head(5))
        #print("aggregate_product_data->container:tail", product_items_container.tail(5))

        return product_items_container

    def process_raw_search_index(self,result:List[Dict[str, Any]]) -> pd.DataFrame:
        """process the raw shopee search data from its api

            Args:
                result:List([Dict[str, Any]]): raw data scrapped from shopee\n

            Returns:
                product_items (pd.DataFrame): search index data

        """
        product_items = {}
        for count, _ in enumerate(result):
            product_items[count] = result[count]['item_basic']
        product_items=pd.DataFrame(product_items).T
        return product_items

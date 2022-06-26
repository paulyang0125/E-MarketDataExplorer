#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality.

Todo:\n
1. very ugly codes too many if-else and for-loop, need to refactor\n
2. move the following jobs to config.py or data_builder.py\n
3. should dynamically represent data_source, not 'shopee'.\n


"""
# shopee_data_explorer/shopee_crawler.py
import ast
import configparser
from pathlib import Path
import json
import logging
import random
#from threading import TIMEOUT_MAX
from typing import Dict, List
from bs4 import BeautifulSoup
import requests
from emarket_data_explorer.classtype import CrawlerHandler
from emarket_data_explorer import (READ_INDEX_ERROR, \
    DATA_FOLDER_WRITE_ERROR,READ_PRODUCT_ERROR, READ_COMMENT_ERROR,SUCCESS)

from emarket_data_explorer.datatype import CrawlerResponse, CrawlerResponseForDict


############# LOGGING #############

mylogger = logging.getLogger(__name__)

fh = logging.FileHandler(f'{__name__}.log')

ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)


class ShopeeCrawlerHandler(CrawlerHandler):
    """ this provides crawler capabilities to read data from shopee"""
    def __init__(self, ip_addresses: List[str] \
        , proxy_auth: str,header: Dict[str, any], webdriver_path: str) -> None:
        super().__init__(ip_addresses,proxy_auth)
        #self.ip_addresses = ip_addresses
        #self.proxy_auth = proxy_auth
        self.header = header
        self.path = webdriver_path
        self.instance_proxies = self._create_header_proxy()


    def __del__(self):
        class_name = self.__class__.__name__
        mylogger.debug("%s is destroyed.", str(class_name))

############# HELPER #############

    def _create_header_proxy(self)-> Dict[str,str]:
        """create the init proxy IP for selenium  """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        return {
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/",
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/"}

    def _rotate_ip(self)-> None:
        """rotate the current IP from the list of proxy ip addresses"""
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        mylogger.debug("The new rotated index: %s", str(proxy_index))
        self.instance_proxies = {
        #"https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index]),
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/",
        #"http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index])}
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/"}

    def _locate_myip(self) -> None:
        """locate my ip"""
        my_ip = requests.get('https://api.ipify.org').text
        mylogger.debug("My public IP address is %s", my_ip)

############# READER #############


    def _fetch(self,session, url, parsing_func):
        """ test """
        raise Exception("not implemented yet")


    async def _download_all_sites(self,sites,parse_func):
        """ test """
        raise Exception("not implemented yet")

    def read_search_indexs(self, keyword: str, page: int, page_length: int) -> CrawlerResponse:
        """read the search result by shopee api

        Args:
            page (int): the iterated number starting from 0, 1, 2, 3, .....etc

        Returns:
            CrawlerResponse

        """
        page = page + 1
        #url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + keyword \
        #+'&limit=' + str(page_length) +'&newest=' + str(page_num*page_length) \
        #    + '&order=desc&page_type=search&version=2'
        url = 'https://shopee.tw/api/v4/search/search_items?by=relevancy&keyword=' \
            + keyword + '&limit=' + str(page_length) + '&newest=' + str(page*page_length) + \
                '&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'

        mylogger.info("reading the search index for %s", str(keyword))
        mylogger.debug("URL is %s", url)


        search_results = None
        retries = 3
        time_out = 5
        while retries > 0:
            try:
                # debug
                #print("2. header type: " + str(type(self.header)))
                #print("2. header items: " + str(self.header.items))
                mylogger.debug("Proxy currently being used: %s", self.instance_proxies['https'])
                search_results = requests.get(url,headers = self.header, proxies=self.\
                    instance_proxies,timeout=(time_out))
            except requests.Timeout:
                mylogger.warning("Timeout Error, looking for another proxy")
                self._rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                mylogger.warning("Connection refused, my ip may be banned! Looking for \
                    another proxy")
                self._rotate_ip()
                retries = retries - 1
            else:
                mylogger.info('reading the search index for %s is completed', keyword)
                mylogger.debug('reading the search index for %s took about %s', keyword, \
                    str(search_results.elapsed.total_seconds()))
                break
        if search_results:
            soup = BeautifulSoup(search_results.content, "html.parser")
            getjson=json.loads(soup.text)
            #debug, will remove
            #print("getjson['items'] type:" + str(type(getjson['items'])))
            mylogger.debug("getjson['itemid']: %s", str(getjson['items'][0]['item_basic']\
                ['itemid']))
            #getjson['items'] is a list
            return CrawlerResponse(getjson['items'],SUCCESS)
        else:
            mylogger.error('reading the index is failed for keyword %s', keyword)
            return CrawlerResponse([],READ_INDEX_ERROR)
            #raise Exception('the cralwer cannot get started, probably your network has issue!')



    def read_good_info(self,shop_id: int, item_id: int) -> CrawlerResponse:
        """ get the good details like articles and SKU by shopee api """

        url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(item_id) + '&shopid=' + \
            str(shop_id)
        mylogger.info('collecting good info for shopid %s and itemid %s', str(item_id), \
            str(shop_id))
        retries = 3
        goods_details_results = None
        time_out = 10
        while retries > 0:
            try:
                mylogger.debug("Proxy currently being used - %s", self.instance_proxies['https'])
                goods_details_results = requests.get(url,headers = self.header,proxies=self.\
                    instance_proxies,timeout=(time_out))
            except requests.Timeout:
                mylogger.warning("requests.Timeout error, looking for another proxy")
                self._rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                mylogger.warning("Connection refused, ip may be banned!")
                self._rotate_ip()
                retries = retries - 1
            else:
                mylogger.info('collecting good info for %s and %s is done ', str(item_id), \
                    str(shop_id))
                mylogger.debug('collecting good info took about %s secs', \
                    str(goods_details_results.elapsed.total_seconds()) )

                #debug
                #print("goods_details_results.text: ", goods_details_results.text)

                break
        if goods_details_results is not None:
            processed_goods = goods_details_results.text.replace("\\n","^n")
            processed_goods = processed_goods.replace("\\t","^t")
            processed_goods = processed_goods.replace("\\r","^r")
            goods_json = json.loads(processed_goods)
            # debug
            #print("goods_jsons: ", str(goods_json))

            #return CrawlerResponse(goods_json,SUCCESS)
            return CrawlerResponseForDict(goods_json,SUCCESS) #goods_json is a dict
        else:
            mylogger.error('collecting good info for %s and %s is failed ', str(item_id), \
                    str(shop_id))
            #return CrawlerResponse({},READ_PRODUCT_ERROR)
            return CrawlerResponseForDict({},READ_PRODUCT_ERROR)


    def read_good_comments(self,shop_id: int, item_id: int) -> CrawlerResponse:
        """get the buyer's comment by using item_id and shop_id by shopee api"""

        url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(item_id) + '&shop_id=' + \
        str(shop_id) + '&offset=0&limit=200&flag=1&filter=0'
        mylogger.info('collecting good comment for shopid %s and itemid %s', str(item_id), \
            str(shop_id))

        retries = 3
        time_out = 15
        comments_results = None
        while retries > 0:
            try:
                mylogger.debug("Proxy currently being used - %s", self.instance_proxies['https'])
                comments_results = requests.get(url,headers = self.header,proxies= \
                    self.instance_proxies,timeout=(time_out))
            except requests.Timeout:
                mylogger.warning("requests.Timeout error, looking for another proxy")
                self._rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                mylogger.warning("Connection refused, ip may be banned!")
                self._rotate_ip()
                retries = retries - 1
            else:
                mylogger.info('collecting the comment for %s and %s is done ', str(item_id), \
                    str(shop_id))
                mylogger.debug('collecting the comment took about %s secs', \
                    str(comments_results.elapsed.total_seconds()) )
                #debug
                #print("comments_results.text: ", comments_results.text)

                break

        if comments_results is not None:
            processed_comments_results= comments_results.text.replace("\\n","^n")
            processed_comments_results=processed_comments_results.replace("\\t","^t")
            processed_comments_results=processed_comments_results.replace("\\r","^r")
            comments_json = json.loads(processed_comments_results)
            # debug
            #print("comments_jsons: ", str(comments_json))
            #comments_json['comments'] is a list
            return CrawlerResponse(comments_json['comments'],SUCCESS)
        else:
            mylogger.error('collecting the comment for %s and %s is failed ', str(item_id), \
                    str(shop_id))
            return CrawlerResponse([],READ_COMMENT_ERROR)

#todo: move the following jobs to config.py or data_builder.py
#todo: should use dynamic to represent data_source, not 'shopee'


def get_data_path(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser(interpolation=None)
    config_parser.read(config_file)
    return Path(config_parser["General"]["shopee_data"])

def get_configs_data(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser(interpolation=None)
    config_parser.read(config_file)
    #myheader = dict(config_parser['Network-Header'].items())

    return Path(config_parser["General"]["shopee_data"]),\
        ast.literal_eval(config_parser["General"]["ip_addresses"]),\
            config_parser["General"]["proxy_auth"],\
                 config_parser["General"]["webdriver_path"],\
                     config_parser["General"]["data_source"],\
                         config_parser["General"]["db_path"],\
                            dict(config_parser['Network-Header'].items())


def init_data(data_path: Path) -> int:
    """Create the shopee_data folder."""
    try:
        data_path.mkdir(parents=True, exist_ok=True)  # create the folder for shopee data
        return SUCCESS
    except OSError:
        return DATA_FOLDER_WRITE_ERROR

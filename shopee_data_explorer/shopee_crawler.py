#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality."""
# shopee_data_explorer/shopee_crawler.py

import configparser
from pathlib import Path
import json
import logging
import random
from typing import Any, Dict, List, NamedTuple
from bs4 import BeautifulSoup
import requests
from shopee_data_explorer import (READ_INDEX_ERROR, DATA_FOLDER_WRITE_ERROR, SUCCESS)

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
mylogger = logging.getLogger(__name__)

DEFAULT_KEYWORD = '運動內衣'
# PAGES stands for the number of pages you want to crawle, 1 page equals to 100 results
DEFAULT_PAGE_NUM = 1
DEFAULT_PAGE_LENGTH = 100
DEFAULT_IP_RANGES = ['45.136.231.43:7099', '45.142.28.20:8031','45.140.13.112:9125',\
    '45.140.13.119:9132', '45.142.28.83:8094','45.136.231.85:7141']
DEFAULT_PROXY_AUTH = "ffpswzty:kvenecq9i6tf"
DEFAULT_HEADER = {'authority' : 'shopee.tw','method': 'GET', \
            'path': '/api/v1/item_detail/?item_id=1147052312&shop_id=17400098', \
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'cookie': '_ga=GA1.2.1087113924.1519696808; SPC_IA=-1; \
            SPC_F=SDsFai6wYMRFvHCNzyBRCvFIp92UnuU3; REC_T_ID=f2be85da-1b61-11e8-a60b-d09466041854;\
            __BWfp=c1519696822183x3c2b15d09; __utmz=88845529.1521362936.1.1.utmcsr=(direct)| \
            utmccn=(direct)|utmcmd=(none); _atrk_siteuid=HEgUlHUKcEXQZWpB; SPC_EC=-; SPC_U=-; \
            SPC_T_ID="vBBUETICFqj4EWefxIdZzfzutfKhrgytH2wyevGxiObL3hFEfy0dpQSOM/yFzaGYQLUANrPe7Q\
            Z4hqLZotPs72MhLd8aK0qhIwD5fqDrlRs="; SPC_T_IV="IpxA2sGrOUQhMH4IaolDSA=="; cto_lwid=2f\
            c9d64c-3cfd-4cf9-9de7-a1516b03ed79; csrftoken=EDL9jQV76T97qmB7PaTPorKtfMlU7eUO; banner\
            Shown=true; _gac_UA-61915057-6=1.1529645767.EAIaIQobChMIwvrkw8bm2wIVkBiPCh2bZAZgEAAYASA\
            AEgIglPD_BwE; _gid=GA1.2.1275115921.1529896103; SPC_SI=2flgu0yh38oo0v2xyzns9a2sk6rz9ou8;\
            __utma=88845529.1087113924.1519696808.1528465088.1529902919.7; __utmc=88845529; \
            appier_utmz=%7B%22csr%22%3A%22(direct)%22%2C%22timestamp%22%3A1529902919%7D; \
            _atrk_sync_cookie=true; _gat=1','if-none-match': "55b03-9ff4fb127aff56426f5ec9022baec5\
            94",'referer': 'https://shopee.tw/6-9-%F0%9F%87%B0%F0%9F%87%B7%E9%9F%93%E5%9C%8B%E9%80%\
            A3%E7%B7%9A-omg!%E6%96%B0%E8%89%B2%E7%99%BB%E5%A0%B4%F0%9F%94%A5%E4%BA%A4%E5%8F%89%E7%BE\
            %8E%E8%83%8CBra%E5%BD%88%E5%8A%9B%E8%83%8C%E5%BF%83-i.17400098.1147052312',\
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/66.0.3359.139 Safari/537.36',
            'x-api-source': 'pc',
            'x-requested-with': 'XMLHttpRequest'
            }


class CrawlerResponse(NamedTuple):
    """data model to controller"""
    result: Dict[str, Any]
    error: int


class CrawlerHandler:
    """ this provides cralwer capabilities to read data from shopee"""
    def __init__(self, ip_addresses: List[str] \
        , proxy_auth: str,header: Dict[str, str]) -> None:
        """ test"""
        self.ip_addresses = ip_addresses
        self.proxy_auth = proxy_auth
        self.header = header
        self.instance_proxies = self._create_header_proxy()

    def __del__(self):
        class_name = self.__class__.__name__
        print(str(class_name) + " is destroyed.")

############# HELPER #############

    def _create_header_proxy(self)-> Dict[str,str]:
        """test"""
        return {
        "https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[0]),
        "http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[0])}

    def _rotate_ip(self)-> None:
        """test"""
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        print("New rotated index: " + str(proxy_index))
        self.instance_proxies = {
        "https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index]),
        "http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index])}

    def _locate_myip(self) -> None:
        """test"""
        my_ip = requests.get('https://api.ipify.org').text
        print(f'My public IP address is: {my_ip}')

############# READER #############

    def read_good_indexs(self, keyword: int, page_num: int, page_length: int) -> CrawlerResponse:
        """
        get the serach result
        page_num: the iterated number starting from 0, 1, 2, 3, .....etc
        """
        page_num = page_num + 1
        url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + keyword \
        +'&limit=' + str(page_length) +'&newest=' + str(page_num*page_length) \
            + '&order=desc&page_type=search&version=2'
        mylogger.info("reading the index for %s", str(keyword))
        mylogger.debug("URL is %s", url)
        #開始請求
        search_results = None
        retries = 3
        time_out = 10
        while retries > 0:
            try:
                mylogger.info("Proxy currently being used: %s", self.instance_proxies['https'])
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
                mylogger.info('reading the index for %s is completed', keyword)
                mylogger.debug('reading the index for %s took about %s', keyword, \
                    str(search_results.elapsed.total_seconds()))
                break
        if search_results is not None:
            soup = BeautifulSoup(search_results.content, "html.parser")
            #將扒下來的文字轉成Json
            getjson=json.loads(soup.text)
            #debug, will remove
            print("getjson['items'] type:" + str(type(getjson['items'])))
            print("getjson['items']['itemid']:" + getjson['items']['itemid'])
            return CrawlerResponse(getjson['items'],SUCCESS)
        else:
            return CrawlerResponse({},READ_INDEX_ERROR)
            #raise Exception('the cralwer cannot get started, probably your network has issue!')



    def read_good_details(self) -> CrawlerResponse:
        """test"""


    def read_good_comments(self) -> CrawlerResponse:
        """test"""


#todo: move the following jobs to config.py or data_builder.py
DEFAULT_DATA_PATH = Path.home().joinpath(
    "Shopee_Data"
)

def get_data_path(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["shopee_data"])

def init_data(data_path: Path) -> int:
    """Create the shopee_data folder."""
    try:
        data_path.mkdir(parents=True, exist_ok=True)  # create the folder for shopee data
        return SUCCESS
    except OSError:
        return DATA_FOLDER_WRITE_ERROR

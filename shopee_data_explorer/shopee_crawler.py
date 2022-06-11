#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality.

Todo:\n
1. very ugly codes too many if-else and for-loop, need to refactor\n
2. move the following jobs to config.py or data_builder.py\n
3. should use dynamic to represent data_source, not 'shopee'


"""
# shopee_data_explorer/shopee_crawler.py
import time
import ast
import configparser
from pathlib import Path
import json
import logging
import random
#from threading import TIMEOUT_MAX
from typing import Any, Dict, List, NamedTuple, Tuple
from bs4 import BeautifulSoup


from seleniumwire import webdriver
import requests
from shopee_data_explorer import (READ_INDEX_ERROR, \
    DATA_FOLDER_WRITE_ERROR,READ_PRODUCT_ERROR, READ_COMMENT_ERROR,SUCCESS)


############# LOGGING #############
#logging.basicConfig(level=logging.WARNING, datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
#logger.setLevel(logging.WARNING)  # or any variant from ERROR, CRITICAL or NOTSET
fh = logging.FileHandler('selenium_debug.log')
#fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


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

############# DEFAULT VARS #############
DEFAULT_KEYWORD = '女性皮夾'
# PAGES stands for the number of pages you want to crawler, 1 page equals to 100 results
DEFAULT_PAGE_NUM = 1
DEFAULT_PAGE_LENGTH = 10
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

DEFAULT_CHROME_WEBDRIVER = '/Users/yao-nienyang/Desktop/Workplace/chromedriver'

############# CLASS IMPLEMENTATION #############

class CrawlerResponse(NamedTuple):
    """data model to Crawler response"""
    result: List[Dict[str, Any]]
    error: int

class CrawlerResponseForDict(NamedTuple):
    """another data model for dict to Crawler response"""
    result: Dict[str, Any]
    error: int

class CrawlerHandler:
    """ this provides crawler capabilities to read data from shopee"""
    def __init__(self, ip_addresses: List[str] \
        , proxy_auth: str,header: Dict[str, any], webdriver_path: str) -> None:
        self.ip_addresses = ip_addresses
        self.proxy_auth = proxy_auth
        self.header = header
        self.path = webdriver_path
        self.instance_proxies = self._create_header_proxy()
        self.seleniumwire_options = self._create_proxy_seleniumwire()
        self.chrome_options = self._setup_chrome_options()

    def __del__(self):
        class_name = self.__class__.__name__
        mylogger.debug("%s is destroyed.", str(class_name))

############# HELPER #############

    def _create_header_proxy(self)-> Dict[str,str]:
        """create the init proxy IP for selenium  """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        return {
        #"https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index]),
        "https": f"https://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/",
        #"http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index])}
        "http": f"http://{self.proxy_auth}@{self.ip_addresses[proxy_index]}/"}

    def _create_proxy_seleniumwire(self) -> Dict[str,Dict[str,str]]:
        """create the init proxy IP for seleniumwire  """
        options = {
                    'proxy': {
                        'http': self.instance_proxies['http'],
                        'https': self.instance_proxies['https'],
                        'no_proxy': 'localhost,127.0.0.1'
                    }}
        return options

    def _setup_chrome_options(self) -> webdriver.ChromeOptions:
        """ set up the headless mode for selenium  """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return chrome_options

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

    def _read_search_results(self,url:str,time_out:int=2) -> str:
        """ read serach results from the shopee search page by selenium """
        mylogger.debug("%s starts.", self._read_search_results.__name__)
        driver = webdriver.Chrome(self.path,options=self.chrome_options,\
            seleniumwire_options=self.seleniumwire_options)
        driver.get(url)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
        time.sleep(time_out)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
        time.sleep(time_out)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
        html = driver.page_source
        driver.quit()
        return html

    def _read_id(self,url:str,time_out:int) -> str:
        """ read shopeid and itemid from shopee page by selenium"""
        mylogger.debug("%s starts.",self._read_id.__name__)
        driver = webdriver.Chrome(self.path,options=self.chrome_options,\
            seleniumwire_options=self.seleniumwire_options)
        #driver = webdriver.Chrome(path,seleniumwire_options=options)
        driver.get(url)
        time.sleep(time_out)
        html = driver.page_source
        driver.quit()
        return html

    def _parse_search_result(self,html:str) -> List[str]:
        """ parse out the url of the product page from shopee """
        mylogger.debug("%s starts.",self._parse_search_result.__name__)
        soup = BeautifulSoup(html,features="html.parser")
        search_product_urls = [i.get('href') for i in soup.find_all('a',\
            attrs={"data-sqe" : "link"}) if i]
        return search_product_urls

    def _parse_itemid(self,html:str) -> Tuple[str,str]:
        """ parse itemid from the shopee product page """
        mylogger.debug("%s starts.",self._parse_itemid.__name__)
        if 'itemId' in html:
            soup = BeautifulSoup(html,features="html.parser")
            for link in soup.find_all('a'):
                if link.get('href') and 'itemId=' in link.get('href'):
                    mylogger.debug("-- %s",str(link.get('href')))
                    #print("-- %s",str(link.get('href')))
                    return (link.get('href'), link.get('href').partition('itemId=')[2])
        else:
            mylogger.warning("can't find itemId")#print(soup.prettify())
            #print("can't find itemId")#print(soup.prettify())
            return ("","")

    # todo: very ugly codes too many if-else and for-loop, need to refactor
    def _parse_shopid(self, html: str):
        """ parse out the shopid from the shopee product page """
        mylogger.debug("%s starts.",self._parse_shopid.__name__)
        if 'shopid' in html:
            if 'shopid=' in html:
                mylogger.debug("shopid=" ": yes")
                #print("shopid=" ": yes")
                mylogger.debug("the content %s",str(html[html.find("shopid="):html.\
                    find("shopid=")+30]))
                #print(str(html[html.find("shopid="):html.find("shopid=")+30]))
                return html[html.find("shopid="):html.find("shopid=")+30].partition("&")\
                    [0].partition("=")[2]
            else:
                soup = BeautifulSoup(html,features="html.parser")
                for link in soup.find_all(['a','link']):
                    if link.get('href'):
                        if 'shopid=' in link.get('href'):
                            mylogger.debug("-- %s",str(link.get('href')))
                            #print("-- %s",str(link.get('href')))
                            shopid = [i.partition('=')[2] for i in link.get('href')\
                                .split('&') if "shopid=" in i]
                            if shopid:
                                return shopid[0]
                        else:
                            return
        else:
            mylogger.warning("can't find shopid")#print(soup.prettify())
            #print("can't find shopid")
            return

    def read_a_page_selenium_search_indexs(self,keyword: int, page: int) -> CrawlerResponse:
        """read a pare of shopee search result - normally it contains 55 results by selenium"""
        mylogger.debug("%s starts.",self.read_a_page_selenium_search_indexs.__name__)
        timeout_1 = 2
        timeout_2 = 3
        timeout_3 = 5
        container = []
        html =  self._read_search_results(f"https://shopee.tw/search?keyword={keyword}\
            &page={page}", timeout_1)
        search_product_urls = self._parse_search_result(html)
        for partial_url in search_product_urls[:5]:
            index = {}
            if partial_url:
                index["product"] = partial_url.partition('-i.')[0]
                url = "https://shopee.tw" + partial_url
                html = self._read_id(url,timeout_2)
                (partial_url,item_id) = self._parse_itemid(html)
                index["item_id"] = item_id
            else:
                partial_url = ""
                index["item_id"] = ""
            if partial_url != "":
                url = "https://shopee.tw" + partial_url
                html = self._read_id(url,timeout_3)
                shopid = self._parse_shopid(html)
                index["shop_id"] = shopid
            else:
                index["shop_id"] = ""
            container.append(index)
        if container:
            return CrawlerResponse(container,SUCCESS)
        else:
            return CrawlerResponse(container,READ_INDEX_ERROR)


    def read_search_indexs(self, keyword: str, page: int, page_length: int) -> CrawlerResponse:
        """read the serach result by shopee api

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
DEFAULT_DATA_PATH = Path.home().joinpath(
    "Shopee_Data"
)

def get_data_path(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser()
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

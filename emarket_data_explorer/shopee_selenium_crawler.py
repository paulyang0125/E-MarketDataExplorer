#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee selenium crawler.

Todo:\n
1. very ugly codes too many if-else and for-loop, need to refactor \n
2. will use multiple thread to enhance the performance in v1.6


"""
# shopee_data_explorer/shopee_selenium_crawler.py
import time
import logging
import random
#from threading import TIMEOUT_MAX
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from seleniumwire import webdriver
import requests
from emarket_data_explorer.classtype import CrawlerHandler
from emarket_data_explorer import (READ_INDEX_ERROR,SUCCESS)

from emarket_data_explorer.datatype import CrawlerResponse


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

###

mylogger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
# create console handler with a higher log level
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)






class ShopeeSeleniumCrawlerHandler(CrawlerHandler):
    """ this provides selenium crawler capabilities to read data from shopee"""

    def __init__(self, ip_addresses: List[str] \
        , proxy_auth: str,header: Dict[str, any], webdriver_path: str) -> None:
        super().__init__(ip_addresses,proxy_auth)
        #self.ip_addresses = ip_addresses
        #self.proxy_auth = proxy_auth
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


    def _fetch(self,session, url, parsing_func):
        """ test """
        raise Exception("not implemented yet")


    async def _download_all_sites(self,sites,parse_func):
        """ test """
        raise Exception("not implemented yet")


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

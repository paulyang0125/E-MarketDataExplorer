#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 13/05/2022
# version ='1.0'
# ---------------------------------------------------------------------------

""" The implementation of Shopee Crawler """


####### utilities #########
import random
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

####### global or from outside #########


####### contant and Instance Variables #########

# KEYWORD is the phrase whih ShopeeCrawler will take to fetch the search results
DEFAULT_KEYWORD = '運動內衣'
# PAGES stands for the number of pages you want to crawle, 1 page equals to 100 results
DEFAULT_PAGE = 2
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





class ShopeeCrawler:
    """ test """
    def __init__(self):
        self.ip_addresses = DEFAULT_IP_RANGES
        self.proxy_auth = DEFAULT_PROXY_AUTH
        self.keyword = DEFAULT_KEYWORD
        self.page = DEFAULT_PAGE
        self.shopee_data_container = pd.DataFrame()
        self.shopee_comment_container =pd.DataFrame()
        self.product_items = []
        self.product_articles = []
        self.product_sku = []
        self.product_tags = []
        self.create_header_proxy()

    def __del__(self):
        class_name = self.__class__.__name__
        print(str(class_name) + " is destroyed.")

##### scraping implmentations ####

    def create_header_proxy(self):
        """ test """
        #封包標頭檔
        self.my_headers = DEFAULT_HEADER

        self.instance_proxies = {
        "https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[0]),
        "http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[0])}

    def rotate_ip(self):
        """ test """
        proxy_index = random.randint(0, len(self.ip_addresses) - 1)
        print("New rotated index: " + str(proxy_index))
        self.instance_proxies = {
        "https": "https://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index]),
        "http": "http://{}@{}/".format(self.proxy_auth, self.ip_addresses[proxy_index])}

    def locate_myip(self):
        """ test """
        my_ip = requests.get('https://api.ipify.org').text
        print(f'My public IP address is: {my_ip}')

    def search_shopee(self,page_num):
        """ get the serach result for 100 products
        - page_num: the iterated number starting from 0, 1, 2, 3, .....etc

        """
        page_num = page_num + 1
        url = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword=' + self.keyword + \
            '&limit=100&newest=' + str(page_num*100) + '&order=desc&page_type=search&version=2'
        print('search_shopee: 正在搜尋： ' + str(self.keyword) + '!')
        #開始請求
        search_results = None
        retries = 3
        time_out = 10
        while retries > 0:
            try:
                print(f"Proxy currently being used: {self.instance_proxies['https']}")
                search_results = requests.get(url,headers = self.my_headers, proxies=self.\
                    instance_proxies,timeout=(time_out))
            except requests.Timeout:
                print("Timeout Error, looking for another proxy")
                self.rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                print("Connection refused, my ip may be banned! Looking for another proxy")
                self.rotate_ip()
                retries = retries - 1
            else:
                print('search_shopee: 爬取完成： ' + self.keyword + '!')
                print('search_shopee的花費時間： ' + str(search_results.elapsed.total_seconds()) )
                break
        if search_results is not None:
            soup = BeautifulSoup(search_results.content, "html.parser")
            #將扒下來的文字轉成Json
            getjson=json.loads(soup.text)
            return getjson['items']
        else:
            raise Exception('the cralwer cannot get started, probably your network has issue!')



    def collect_good_details(self,item_id, shop_id):
        """ get the details like articles and SKU """

        url = 'https://shopee.tw/api/v2/item/get?itemid=' + str(item_id) + '&shopid=' + str(shop_id)
        print('collect_good_details: 正在爬取商品： ' + str(item_id) + " : " + str(shop_id) +'!')
        retries = 3
        goods_details_results = None
        time_out = 10
        while retries > 0:
            try:
                print(f"Proxy currently being used: {self.instance_proxies['https']}")
                goods_details_results = requests.get(url,headers = self.my_headers,proxies=self.\
                    instance_proxies,timeout=(time_out))
            except requests.Timeout:
                print("requests.Timeout error, looking for another proxy")
                self.rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                print("Connection refused, ip may be banned!")
                self.rotate_ip()
                retries = retries - 1
            else:
                print('collect_good_details: 爬取商品完成： ' + str(item_id) + " : " + str(shop_id)  \
                    + '!')
                print('collect_good_details的花費時間： ' + str(goods_details_results.elapsed. \
                    total_seconds()) )
                break
        if goods_details_results is not None:
            processed_goods = goods_details_results.text.replace("\\n","^n")
            processed_goods = processed_goods.replace("\\t","^t")
            processed_goods = processed_goods.replace("\\r","^r")
            goods_json = json.loads(processed_goods)
            return goods_json['item']
        else:
            print('collect_good_details: 爬取商品失敗')
            return {}


    def collect_good_comments(self,item_id,shop_id):
        """get the buyer's comment by using item_id and shop_id"""

        url = 'https://shopee.tw/api/v1/comment_list/?item_id='+ str(item_id) + '&shop_id=' + \
        str(shop_id) + '&offset=0&limit=200&flag=1&filter=0'
        print('collect_good_comments: 正在爬取商品： ' + str(item_id) + " : " + str(shop_id) + '!')
        retries = 3
        time_out = 15
        comments_results = None
        while retries > 0:
            try:
                print(f"Proxy currently being used: {self.instance_proxies['https']}")
                comments_results = requests.get(url,headers = self.my_headers,proxies= \
                    self.instance_proxies,timeout=(time_out))
            except requests.Timeout:
                print("requests.Timeout error, looking for another proxy")
                self.rotate_ip()
                retries = retries - 1
            except requests.exceptions.ConnectionError:
                print("Connection refused, ip may be banned!")
                self.rotate_ip()
                retries = retries - 1
            else:
                print('collect_good_comments: 爬取商品完成： ' + str(item_id) + " : " + str(shop_id) \
                     + '!')
                print('collect_good_comments的花費時間： ' + str(comments_results.elapsed. \
                    total_seconds()))
                break

        if comments_results is not None:
            processed_comments_results= comments_results.text.replace("\\n","^n")
            processed_comments_results=processed_comments_results.replace("\\t","^t")
            processed_comments_results=processed_comments_results.replace("\\r","^r")
            comments_json = json.loads(processed_comments_results)
            return comments_json['comments']
        else:
            print('collect_good_comments: 爬取商品失敗')
            return {}

    ##### data process ####

    def process_shopee_prodcts(self,product):
        """ test """
        if product:
            self.product_articles.append(product['description'])
            self.product_sku.append(product['models'])
            self.product_tags.append(product['hashtag_list'])
        else:
            self.product_articles.append('na')
            self.product_sku.append('na')
            self.product_tags.append('na')


    def process_shopee_comment(self,comment):
        """ test """

        user_comment = pd.DataFrame(comment) #covert comment to data frame

        if not user_comment.empty:
            models=[]
            for item in user_comment['product_items']:
                if pd.DataFrame(item).filter(regex = 'model_name').shape[1] != 0:
                    models.append(pd.DataFrame(item)['model_name'].tolist())
                else:
                    print('No model_name')
                    models.append(None)

            user_comment['product_items']= models # puts models aka SKUs in

        self.shopee_comment_container = pd.concat([self.shopee_comment_container, user_comment], \
            axis= 0)

    def clean_product_data(self):
        """ test """
        self.product_articles= []
        self.product_sku= []
        self.product_tags = []

    def finalize_shopee_product(self):
        """ merge product details with the search results for one page - 100 results per loop """



        # using pd.Series is to avoid Value error which occurs when you the number of a list like
        # product_sku as input is not matched with the number of row of product_items,
        # for example, product_sku: 50 != product_items['SKU']: 100. Series will
        # fill NA automatically for the missing rows

        self.product_items['articles'] = pd.Series(self.product_articles)
        self.product_items['SKU'] = pd.Series(self.product_sku)
        self.product_items['hashtag_list'] = pd.Series(self.product_tags)
        #self.product_items['articles'] = self.product_articles
        #self.product_items['SKU'] = self.product_sku
        #self.product_items['hashtag_list'] = self.product_tags
        self.shopee_data_container = pd.concat([self.shopee_data_container, self.product_items],\
            axis=0)

    def scrap_shopee_search_results(self, i):
        """get 100 search results"""
        self.product_items=pd.DataFrame(self.search_shopee(i))
        print("scrap_shopee_search_results: 取得" + str(len(self.product_items['itemid'].tolist())) \
             + "筆搜尋結果")

    ##### end process ####
    def write_shopee_goods_data(self):
        """ test """
        self.shopee_data_container.to_csv('shopee_' + self.keyword +'_goods_data.csv', encoding \
        = 'utf-8-sig')

    def write_shopee_comments_data(self):
        """ test """
        self.shopee_comment_container.to_csv('shopee_' + self.keyword +'_comments_data.csv', \
            encoding = 'utf-8-sig')


##### three scaping workflows ####

    def scrap_shopee_all(self):
        """get ALL mode"""
        for i in tqdm(range(self.page)):
            print("## 第" + str(i) + "回抓取 ##" )
            self.scrap_shopee_search_results(i)
            for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist(), \
            self.product_items['shopid'].tolist(),self.product_items['name'].tolist()) \
            ,total=len(self.product_items['itemid'].tolist())):
                print('正在爬取商品： ' + name[:30] + '...')
                product=self.collect_good_details(item_id = itemid, shop_id = shopid)
                self.process_shopee_prodcts(product)
                comments = self.collect_good_comments(item_id = itemid, shop_id = shopid)
                self.process_shopee_comment(comments)
            self.finalize_shopee_product()
            self.clean_product_data()
            self.write_shopee_goods_data()
            self.write_shopee_comments_data()
        #self.clean_data()

    def scrap_shopee_all_debug(self):
        """get ALL but retrive only 10 for a page for debugging"""
        for i in tqdm(range(self.page)):
            print("## 第" + str(i) + "回抓取 ##" )
            self.scrap_shopee_search_results(i)
            for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist()[:10], \
            self.product_items['shopid'].tolist()[:10],self.product_items['name'].tolist()[:10]) \
            ,total=len(self.product_items['itemid'].tolist()[:10])):
                print('正在爬取商品： ' + name[:30] + '...')
                product=self.collect_good_details(item_id = itemid, shop_id = shopid)
                self.process_shopee_prodcts(product)
                comments = self.collect_good_comments(item_id = itemid, shop_id = shopid)
                self.process_shopee_comment(comments)
            self.finalize_shopee_product()
            self.clean_product_data()
            self.write_shopee_goods_data()
            self.write_shopee_comments_data()


    def scrap_shopee_goods(self):
        """ get goods mode"""
        for i in tqdm(range(self.page)):
            print("## 第" + str(i) + "回抓取 ##" )
            self.scrap_shopee_search_results(i)
            for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist(), \
            self.product_items['shopid'].tolist(),self.product_items['name'].tolist()) \
                ,total=len(self.product_items['itemid'].tolist())):
                print('正在爬取商品： ' + name[:30] + '...')
                product=self.collect_good_details(item_id = itemid, shop_id = shopid)
                self.process_shopee_prodcts(product)
            self.finalize_shopee_product()
            self.clean_product_data()
            self.write_shopee_goods_data()

    def scrap_shopee_comments(self):
        """ get comments mode """
        for i in tqdm(range(self.page)):
            print("## 第" + str(i) + "回抓取 ##" )
            self.scrap_shopee_search_results(i)
            for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist(), \
            self.product_items['shopid'].tolist(),self.product_items['name'].tolist()),\
                total=len(self.product_items['itemid'].tolist())):
                print('正在爬取商品： ' + name[:30] + '...')
                comments = self.collect_good_comments(item_id = itemid, shop_id = shopid)
                self.process_shopee_comment(comments)
            self.write_shopee_comments_data()



####### testing #########

crawler_instance = ShopeeCrawler()
crawler_instance.scrap_shopee_goods()
del crawler_instance
crawler_instance = ShopeeCrawler()
crawler_instance.scrap_shopee_comments()
del crawler_instance


'''
crawler_instance = ShopeeCrawler()
crawler_instance.scrap_shopee_all_debug()
del crawler_instance
'''
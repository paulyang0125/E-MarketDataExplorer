############## INPUTS
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
'''
##init

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

'''


############## PROCESSES and OUTPUTS
'''

class CrawlerResponse(NamedTuple):
    """data model to controller"""
    todo_list: Dict[str, Any]
    error: int


class CrawlerHandler:

class CrawlerDataProcesser:

//

#getter

1. search_shopee(self,page_num): -> getjson['items']:json Aka a index with print for
thing doing, exception, time consumed
// one page == 100 search results is less flexbiuble
// define page_length as input? and set DEFAULT_LENGTH = 100
// rename to read_good_indexs()

2. collect_good_details(self,item_id, shop_id): ->goods_json['item']:json with prints
// rename to read_good_details()


3. collect_good_comments(self,item_id,shop_id): -> comments_json['comments']:json with prints
// rename to read_good_comments()



#processer



5. scrap_shopee_search_results(self, page_num:int) - > None (actually self.product_items)
        """define one page == 100 search results"""
        self.product_items=pd.DataFrame(self.search_shopee(page_num)) //belong to data proceessor
        print("scrap_shopee_search_results: 取得" + str(len(self.product_items['itemid'].tolist())) \
             + "筆搜尋結果") //this should belong to workflower

            //

1. process_shopee_prodcts(self,product):->None, extract description, models, hashtag_list

            self.product_articles.append(product['description'])
            self.product_sku.append(product['models'])
            self.product_tags.append(product['hashtag_list'])


3. clean_product_data(self): => None, clean three instance arraies: product_article[],
product_sku[],product_tags[]


4. finalize_shopee_product(self):->None, merge product details with the
search results for one page - 100 results per loop

        self.product_items['articles'] = pd.Series(self.product_articles)
        self.product_items['SKU'] = pd.Series(self.product_sku)
        self.product_items['hashtag_list'] = pd.Series(self.product_tags)
        self.shopee_data_container = pd.concat([self.shopee_data_container, self.product_items],\
            axis=0)


2. process_shopee_comment(self,comment): -> None, extract model_name and
concat to shopee_comment_container

    models.append(pd.DataFrame(item)['model_name'].tolist())
    user_comment['product_items']= models # puts models aka SKUs in
    self.shopee_comment_container = pd.concat([self.shopee_comment_container, user_comment], \
            axis= 0)

# aggregators

self.shopee_data_container
self.shopee_comment_container


##### three scaping workflows ####

1. scrap_shopee_all(self):
    for i in tqdm(range(self.page)):
         print("## 第" + str(i) + "回抓取 ##" )
        self.scrap_shopee_search_results(i)
        for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist(),....):
            print('正在爬取商品： ' + name[:30] + '...')
                product=self.collect_good_details(item_id = itemid, shop_id = shopid)
                self.process_shopee_prodcts(product)
                comments = self.collect_good_comments(item_id = itemid, shop_id = shopid)
                self.process_shopee_comment(comments)
            self.finalize_shopee_product()
            self.clean_product_data()
            self.write_shopee_goods_data()
            self.write_shopee_comments_data()


2. scrap_shopee_all_debug(self):
        """get ALL but retrive only 10 for a page for debugging"""
        for itemid, shopid, name in tqdm(zip(self.product_items['itemid'].tolist()[:10], \


3. scrap_shopee_goods(self):


4. scrap_shopee_comments(self)


## helpers

    def create_header_proxy(self):

    def rotate_ip(self):

    def locate_myip(self):




##### write process ####

1. write_shopee_goods_data(self):
    self.shopee_data_container.to_csv('shopee_' + self.keyword +'_goods_data.csv', encoding \
    = 'utf-8-sig')

2. write_shopee_comments_data(self):
        self.shopee_comment_container.to_csv('shopee_' + self.keyword +'_comments_data.csv', \
            encoding = 'utf-8-sig')


'''
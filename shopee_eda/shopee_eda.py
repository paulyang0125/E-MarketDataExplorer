#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 18/05/2022
# version ='1.0'
# ---------------------------------------------------------------------------

""" The implementation of Shopee EDA """

####### utilities #########
import random
import platform
import base64
from io import BytesIO
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np



'''
objectives:

a. data preprocessing
b. create the following figures
    1. Price vs. Historical Sales - the analsys of product price and sales
    2. Star Rating vs. Sum of Rating Items - the comparison of rating products
    3. Total amount of money spent vs. Average purchase price - the Summary of Consumer Purchasing Power
    4. Average purchase price vs. Total amount of customer - the Deep-dive of Consumer Purchasing Power
    5. Tag Name vs. Total usage - the tag rankings
    6. Total amount of a tag vs. total amount of sales - the corelationship of tags and sales

'''

####### global or from outside #########


class ShopeeEDA():
    """ test """
    ####### contant and Instance Variables ########

    def __init__(self,charts, comments, contents,myfont,chart_color=None):
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        if not chart_color:
            self.colors_group = ['#427f8f','#8B0000','#559db0','#8B0000','#0000FF','#FF6347',\
            '#006400','#4682B4','#4169E1','#D2691E']
            self.chart_color = self.rotate_color()
        else:
            self.chart_color = chart_color
        self.comments = comments
        self.contents = contents
        self.myfont = myfont
        self.contents_final = pd.DataFrame()
        self.comments_final = pd.DataFrame()
        self.tag_data = pd.DataFrame()
        self.consumer_power = pd.DataFrame()
        self.charts = charts

    def rotate_color(self):
        """ test """
        color_index = random.randint(0, len(self.colors_group) - 1)
        print("New color index: " + str(color_index))
        return self.colors_group[color_index]

    def clean_data(self):
        """ test """
        # divide price by 100000
        self.contents['price'] = self.contents['price'] / 100000


    def create_tags(self):
        """ test """
        tag_list = []
        for i in self.contents['articles']:
            if isinstance(i,str):
                tagg = i.split('#')
                tagg = tagg[1::]
                tagg = [g.replace(' ','') for g in tagg]
            else:
                tagg = []

            tag_list.append(tagg)

        self.contents['Tag'] = tag_list

    def evaluation(self,thestr):
        """
        建立evaluation函數，讓後續「字詞」可以轉「原始形態」，
        例如： 字串形態的'{'A':1}' -->  字典形態的 {'A':1}
        """
        return eval(thestr)

    def process_rating(self):
        """把欄位的內容放入evaluation方法進行轉換"""
        self.contents['item_rating'] = self.contents['item_rating'].apply(self.evaluation)
        self.contents['rating_star'] = self.contents['item_rating']\
            .apply(lambda x:x['rating_star'])
        self.contents['rating_numbers'] = self.contents['item_rating']\
            .apply(lambda x:np.sum( \
        x['rating_count']))

    def create_preprocessed_dataframes(self):
        """ test """
        # put sku（商品規格）into content
        comment_sku = self.comments.drop_duplicates('itemid')
        self.contents = self.contents.merge(comment_sku[['itemid', 'product_items']], \
        how = 'left', on='itemid')
        # get out the key columns from contents
        self.contents_final = self.contents[['itemid','name','brand','Tag' ,'price', \
            'historical_sold',\
            'articles', 'shopid','rating_numbers','rating_star','liked_count']]
        # mege content的'itemid', 'price','name'to comment
        self.comments = self.comments.merge(self.contents[['itemid', 'price','name']], \
        how = 'left', on='itemid')
        # issue：remove duplicatied items
        # hint：drop_duplicates
        self.comments = self.comments.drop_duplicates()
        # get the key columns for comments_final
        self.comments_final = self.comments[['itemid',	'shopid',	'name',	'price',\
            'userid','ctime','orderid', 'rating_star', 'comment','product_items']]
        self.save_preprocessed_dataframes()

    def save_preprocessed_dataframes(self):
        """ test """
        shopee_product_name = "shopee_processed_product_data.csv"
        shopee_comment_name = "shopee_processed_comment_data.csv"
        self.contents_final.to_csv(shopee_product_name,encoding = 'UTF-8-sig')
        self.comments_final.to_csv(shopee_comment_name,encoding= 'UTF-8-sig')

    def do_eda(self):
        """ test """
        # preprocessing
        print("1. start preprocessing!")
        self.clean_data()
        self.create_tags()
        self.process_rating()
        self.create_preprocessed_dataframes()
        # drawing
        print("2. start drawing!")
        self.prepare_figures_header()
        self.make_figures(self.charts)

    def make_figures(self,charts:list) -> None:
        """ test """
        candidates = [self.make_figure1, self.make_figure2, \
            self.make_figure3,self.make_figure4,self.make_figure5,self.make_figure6]
        for index, _ in enumerate(charts):
            if charts[index] in candidates[index].__name__:
                candidates[index]()

    def prepare_figures_header(self):
        """ test """
        html = '<h1 style="font-size:60px; text-align:center;">Shopee EDA charts</h1>\n'
        with open('test.html','w',encoding="utf-8") as htm_file:
            htm_file.write(html)

    def make_pics_html(self, fig_object,num):
        """ test """
        tmpfile = BytesIO()
        fig_object.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        #html = '<img src=\'data:image/png;base64,{}\'>\n'.format(encoded)
        html = f'<img src=\'data:image/png;base64,{encoded}\'>\n'
        with open('test.html','a',encoding="utf-8") as htm_file:
            htm_file.write(html)
        fig_object.savefig(f'figure{str(num)}.png', bbox_inches='tight')

    def make_figure1(self):
        """ test """
        plt.figure( figsize = (10,6))
        plt.scatter(self.contents_final['price'],self.contents_final['historical_sold'],
            color=self.chart_color,alpha=0.5)
        plt.title("Analsys of product prices and sales",fontsize=30,)
        plt.ylabel("Historical Sales",fontsize=20,)
        plt.xlabel("Price",fontsize=20,)
        plt.grid(True)
        plt.tight_layout()
        self.make_pics_html(plt,1)


    def make_figure2(self):
        """ test """
        product_data_melt_zero = self.contents_final[self.contents_final['rating_star']>3]
        plt.figure( figsize = (10,6))
        plt.scatter(product_data_melt_zero['rating_star'],product_data_melt_zero['rating_numbers'],
            color=self.chart_color,
            alpha=0.5)
        plt.title("Comparison of rating products",fontsize=30,fontproperties=self.myfont)
        plt.ylabel("Sum of Rating Items",fontsize=20,fontproperties=self.myfont)
        plt.xlabel("Star Rating",fontsize=20,fontproperties=self.myfont)
        plt.grid(True)
        plt.tight_layout()
        self.make_pics_html(plt,2)

    def make_figure3(self):
        """ test """
        self.consumer_power = self.comments_final[['userid','price']].groupby('userid').sum()
        self.consumer_power = pd.concat([self.consumer_power,self.comments_final[['userid',\
            'price']].groupby('userid').mean()], axis=1)
        self.consumer_power.columns = ['total_amount_of_money_spent','avg_purchase_price']
        plt.figure( figsize = (10,6))
        plt.scatter(self.consumer_power['avg_purchase_price'],self.consumer_power\
            ['total_amount_of_money_spent'],
            color=self.chart_color,
            alpha=0.5)
        plt.title("Summary of Consumer Purchasing Power",fontsize=30,fontproperties=self.myfont)
        plt.xlabel("Average purchase price",fontsize=20,fontproperties=self.myfont)
        plt.ylabel("Total amount of money spent",fontsize=20,fontproperties=self.myfont)
        plt.grid(True)
        plt.tight_layout()
        self.make_pics_html(plt,3)


    def make_figure4(self):
        """ test """
        consumer_power_interval = pd.DataFrame(self.consumer_power['avg_purchase_price']\
            .value_counts())
        consumer_power_interval.sort_index(inplace=True)
        consumer_power_interval.columns = ['total_amount_of_customer']
        plt.figure( figsize = (10,6))
        plt.scatter(consumer_power_interval.index,consumer_power_interval,color=self.chart_color)
        plt.title("Deep-dive of Consumer Purchasing Power",fontsize=30,fontproperties=self\
            .myfont)
        plt.xlabel("Average purchase price",fontsize=20,fontproperties=self.myfont)
        plt.ylabel("Total amount of customer",fontsize=20,fontproperties=self.myfont)
        plt.grid(True)
        plt.tight_layout()
        self.make_pics_html(plt,4)


    def make_figure5(self):
        """ test """
        tags_list = []
        count_list = []
        like_list = []
        sale_list = []
        for tags,likes,his_sold in zip(self.contents_final['Tag'].tolist(), \
            self.contents_final['liked_count'].tolist()\
            ,self.contents_final['historical_sold'].tolist()):
            #print("i: " + str(type(i)))
            if not isinstance(tags, list):
                tags = eval(tags)

            for tag in tags:
                # if not repeate, add the new tag to the four lists
                if tag not in tags_list and tag:
                    tags_list.append(tag)
                    count_list.append(1)
                    like_list.append(likes)
                    sale_list.append(his_sold)
                # if repeate, increase the numbers for that repeated tag in count_list、\
                # like_list、sale_list
                else:
                    if tag:
                        count_list[tags_list.index(tag)] = count_list[tags_list.index(tag)]+1
                        like_list[tags_list.index(tag)] = like_list[tags_list.index(tag)]+likes
                        sale_list[tags_list.index(tag)] = sale_list[tags_list.index(tag)]+his_sold

        dic = {
            'Tag': tags_list,
            'total_usage':count_list,
            'total_likes':like_list,
            'sales':sale_list
            }

        self.tag_data = pd.DataFrame(dic)
        self.tag_data =  self.tag_data.sort_values(by=['total_usage'], ascending = False)
        print(self.tag_data['Tag'][:10])
        plt.figure( figsize = (10,6))
        plt.bar(self.tag_data['Tag'][:10],  self.tag_data['total_usage'][:10])
        plt.title("Tag rankings",fontsize=30,fontproperties=self.myfont)
        plt.xlabel("Tag Name",fontsize=20,fontproperties=self.myfont)
        plt.ylabel("Total Usage",fontsize=20,fontproperties=self.myfont)
        plt.xticks(fontsize=20,rotation=90)
        plt.tight_layout()
        self.make_pics_html(plt,5)



    def make_figure6(self):
        """ test """
        plt.figure( figsize = (10,6))
        plt.scatter(self.tag_data['total_likes'],self.tag_data['sales'],color=self.chart_color)
        plt.title("Corelationship between tags and sales",fontsize=30,fontproperties=self.myfont)#標題
        for like,sale,tag in zip(self.tag_data['total_likes'],self.tag_data['sales'],\
            self.tag_data['Tag']):
            if like > self.tag_data['total_likes'].mean()+self.tag_data['total_likes'].std()*1 \
                and sale > self.tag_data['sales'].mean()+self.tag_data['sales'].std()*1:
                plt.text(like, sale, tag, fontsize=12,) # annotate the tag name on the last day
        plt.xlabel("Like Counts",fontsize=20,)
        plt.ylabel("Total amount of sales",fontsize=20,)
        plt.grid(True)
        plt.tight_layout()
        self.make_pics_html(plt,6)

###test###



# 判斷是甚麼作業系統
THE_OS = list(platform.uname())[0]
if THE_OS == 'Windows':
    THE_OS = '\\'
    ECODE = 'utf-8-sig'
elif THE_OS == 'Darwin':
    THE_OS = '/'
    ECODE = 'utf-8-sig'
else:
    THE_OS = '/'
    ECODE = 'utf-8'

font = FontProperties(fname='tools'+ THE_OS + 'msj.ttf')

#讀取原始檔案
test_comments = pd.read_csv('data' + THE_OS + '蝦皮_運動內衣_留言資料.csv',encoding = ECODE, engine= 'python')
test_contents = pd.read_csv('data' + THE_OS + '蝦皮_運動內衣_商品資料.csv',encoding = ECODE, engine= 'python')
chart_groups = ['make_figure1', 'make_figure2', 'make_figure3','make_figure4',\
     'make_figure5', 'make_figure6']
shopee_eda_instance = ShopeeEDA(chart_groups,test_comments,test_contents,font)
shopee_eda_instance.do_eda()

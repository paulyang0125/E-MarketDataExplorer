#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 18/05/2022
# version ='1.0'
# ---------------------------------------------------------------------------

""" The implementation of Shopee EDA """

####### utilities #########
import platform
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np

####### global or from outside #########


class ShopeeEDA():
    """ test """
    ####### contant and Instance Variables ########

    def __init__(self, comments, contents,myfont):
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.colors_group = ['#427f8f','#4a8fa1','#559db0','#66a7b8','#77b1c0','#89bbc8','#9ac5d0',\
        '#bdd9e0','#cee3e8','#e0edf0']
        self.comments = comments
        self.contents = contents
        self.myfont = myfont
        self.contents_final = pd.DataFrame()
        self.comments_final = pd.DataFrame()
        self.tag_data = pd.DataFrame()
        self.consumer_power = pd.DataFrame()

    def clean_data(self):
        """ test """
        self.contents= self.contents.rename(columns = {'itemid':'商品ID', # 關聯留言資料時可以用
                                    'price':'價格', # 計算市場區隔用
                                    'shopid':'賣家ID', # 關聯資料用
                                    'brand':'品牌', # 進行市場定位時可以進行競爭比較
                                    'articles':'商品文案', # 爲消費者定義tag可以用
                                    'liked_count':'喜愛數量', # 蝦皮網站基礎分析
                                    'historical_sold':'歷史銷售量', # 計算市場區隔用
                                    'name':'商品名稱'}  ) # 計算市場區隔用
        # 將價格除以100000，然後存回價格欄位
        self.contents['價格'] = self.contents['價格'] / 100000

        self.comments = self.comments.rename(columns = {
                'itemid':'商品ID',
                'shopid':'賣家ID',
                'userid':'使用者ID',
                'ctime':'留言時間',
                'is_hidden':'是否隱藏',
                'orderid':'訂單編號',
                'rating_star':'給星',
                'comment':'留言內容',
                'product_items':'商品規格'
            })





    def create_tags(self):
        """ test """
        # 處理Tag
        tag_list = []
        for i in self.contents['商品文案']:
            if isinstance(i,str):
                tagg = i.split('#')
                tagg = tagg[1::]
                # 將空白取代掉
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
        # 將item_rating字典裏面的rating_star取出，並命名爲「評分」
        self.contents['評分'] = self.contents['item_rating'].apply(lambda x:x['rating_star'])
        self.contents['評價數量'] = self.contents['item_rating'].apply(lambda x:np.sum( \
        x['rating_count']))

    def create_preprocessed_dataframes(self):
        """ test """
        # 將sku（商品規格）融入content裏面
        comment_sku = self.comments.drop_duplicates('商品ID')
        self.contents = self.contents.merge(comment_sku[['商品ID', '商品規格']], how = 'left', on='商品ID')
        # 特別將content的部分欄位取出
        self.contents_final = self.contents[['商品ID','商品名稱','品牌','Tag' ,'價格', '歷史銷售量',\
            '商品文案', '賣家ID','評價數量','評分','喜愛數量']]
        # 將content的'商品ID', '價格','折扣'融入到comment
        self.comments = self.comments.merge(self.contents[['商品ID', '價格','商品名稱']], how = 'left' \
            , on='商品ID')
        # 問題：有一些comment是重複爬取的要刪除,並存回
        # hint：drop_duplicates
        self.comments = self.comments.drop_duplicates()
        # 特別將comment的部分欄位取出
        self.comments_final = self.comments[['商品ID',	'賣家ID',	'商品名稱',	'價格',	'使用者ID', \
             '留言時間','訂單編號', '給星', '留言內容','商品規格']]
        self.save_preprocessed_dataframes()

    def save_preprocessed_dataframes(self):
        """ test """
        # 問題：將content_final存儲為 '蝦皮_運動內衣_【處理後】商品資料.csv'
        self.contents_final.to_csv('蝦皮_運動內衣_【處理後】商品資料.csv',encoding = 'UTF-8-sig')
        self.comments_final.to_csv('蝦皮_運動內衣_【處理後】留言資料.csv',encoding= 'UTF-8-sig')

    def do_eda(self):
        """ test """
        # preprocessing
        self.clean_data()
        self.create_tags()
        self.process_rating()
        self.create_preprocessed_dataframes()
        # drawing
        self.make_figure1()
        self.make_figure2()
        self.make_figure3()
        self.make_figure4()
        self.make_figure5()
        self.make_figure6()

    def make_figure1(self):
        """ test """
        plt.figure( figsize = (10,6))
        plt.scatter(self.contents_final['價格'],self.contents_final['歷史銷售量'],
            color=self.colors_group[0],alpha=0.5)
        plt.title("商品價格與銷售量分析圖",fontsize=30,)#標題
        plt.ylabel("銷售量",fontsize=20,)#y的標題
        plt.xlabel("價格",fontsize=20,) #x的標題
        plt.grid(True) # grid 開啟
        plt.tight_layout()
        plt.savefig('figure1.png', bbox_inches='tight')

    def make_figure2(self):
        """ test """
        product_data_melt_zero = self.contents_final[self.contents_final['評分']>3]
        plt.figure( figsize = (10,6))
        plt.scatter(product_data_melt_zero['評分'],product_data_melt_zero['評價數量'],
            color=self.colors_group[0],
            alpha=0.5)
        plt.title("商品評分評價比較圖",fontsize=30,fontproperties=self.myfont)#標題
        plt.ylabel("評價數量",fontsize=20,fontproperties=self.myfont)#y的標題
        plt.xlabel("評分",fontsize=20,fontproperties=self.myfont) #x的標題
        plt.grid(True) # grid 開啟
        plt.tight_layout()
        plt.savefig('figure2.png', bbox_inches='tight')

    def make_figure3(self):
        """ test """
        self.consumer_power = self.comments_final[['使用者ID','價格']].groupby("使用者ID").sum()
        self.consumer_power = pd.concat([self.consumer_power,self.comments_final[['使用者ID','價格'\
            ]].groupby("使用者ID").mean()], axis=1)
        self.consumer_power.columns = ['總購買金額','平均購買金額']
        plt.figure( figsize = (10,6))
        plt.scatter(self.consumer_power['平均購買金額'],self.consumer_power['總購買金額'],
            color=self.colors_group[0],
            alpha=0.5)
        plt.title("消費者購買力分析圖",fontsize=30,fontproperties=self.myfont)#標題
        plt.xlabel("平均購買金額",fontsize=20,fontproperties=self.myfont)#y的標題
        plt.ylabel("總購買金額",fontsize=20,fontproperties=self.myfont) #x的標題
        plt.grid(True) # grid 開啟
        plt.tight_layout()
        plt.savefig('figure3.png', bbox_inches='tight')

    def make_figure4(self):
        """ test """
        consumer_power_interval = pd.DataFrame(self.consumer_power['平均購買金額'].value_counts())
        consumer_power_interval.sort_index(inplace=True)
        consumer_power_interval.columns = ['每個平均價格下的購買人數']
        plt.figure( figsize = (10,6))
        plt.plot(consumer_power_interval.index,consumer_power_interval,color=self.colors_group[0])
        plt.title("消費者購買力剖析（價格區間）",fontsize=30,fontproperties=self.myfont)#標題
        plt.xlabel("平均購買金額",fontsize=20,fontproperties=self.myfont)#y的標題
        plt.ylabel("人數",fontsize=20,fontproperties=self.myfont) #x的標題
        plt.grid(True) # grid 開啟
        plt.tight_layout()
        plt.savefig('figure4.png', bbox_inches='tight')

    def make_figure5(self):
        """ test """
        tag = []
        count = []
        like = []
        sale = []
        for i,l,h in zip(self.contents_final['Tag'].tolist(), self.contents_final['喜愛數量'].tolist()\
            ,self.contents_final['歷史銷售量'].tolist()):
            #print("i: " + str(type(i)))
            if not isinstance(i, list):
                i = eval(i)

            for j in i:
                # 如果沒有重複，則將「新的tag」新增進去tag陣列
                if j not in tag:
                    tag.append(j)
                    count.append(1)
                    like.append(l)
                    sale.append(h)

                # 如果該tag先前已經有重複，則將其從過往的陣列索引（index）中找出，對count、like、sale三個變數再行加總
                else:
                    count[tag.index(j)] = count[tag.index(j)]+1
                    like[tag.index(j)] = like[tag.index(j)]+l
                    sale[tag.index(j)] = sale[tag.index(j)]+h

        dic = {
            'Tag':tag,
            '總使用數量':count,
            '總喜歡數':like,
            '總銷量':sale
            }
        self.tag_data = pd.DataFrame(dic)
        self.tag_data =  self.tag_data.sort_values(by=['總使用數量'], ascending = False)

        plt.figure( figsize = (10,6))
        plt.bar(self.tag_data['Tag'][:10],  self.tag_data['總使用數量'][:10])
        plt.title("Tag使用排行",fontsize=30,fontproperties=self.myfont)#標題
        plt.xlabel("Tag名稱",fontsize=20,)#y的標題
        plt.ylabel("總使用數量",fontsize=20,) #x的標題
        plt.xticks(fontsize=20,rotation=90)
        plt.tight_layout()
        plt.savefig('figure5.png', bbox_inches='tight')

    def make_figure6(self):
        """ test """
        plt.figure( figsize = (10,6))
        plt.scatter(self.tag_data['總喜歡數'],self.tag_data['總銷量'],color=self.colors_group[0])
        plt.title("Tag的喜歡與總銷量比較圖",fontsize=30,fontproperties=self.myfont)#標題
        for i,j,t in zip(self.tag_data['總喜歡數'],self.tag_data['總銷量'],self.tag_data['Tag']):
            if i > self.tag_data['總喜歡數'].mean()+self.tag_data['總喜歡數'].std()*1 and j > \
                self.tag_data['總銷量'].mean()+self.tag_data['總銷量'].std()*1:
                plt.text(i, j, t, fontsize=12,) # 最後一天的點上方的標籤文字
        plt.xlabel("總喜歡數",fontsize=20,)#y的標題
        plt.ylabel("總銷量",fontsize=20,) #x的標題
        plt.grid(True) # grid 開啟
        plt.tight_layout()
        plt.savefig('figure6.png', bbox_inches='tight')


###test###

# 判斷是甚麼作業系統
theOS = list(platform.uname())[0]
if theOS == 'Windows':
    theOS = '\\'
    ecode = 'utf-8-sig'
elif theOS == 'Darwin':
    theOS = '/'
    ecode = 'utf-8-sig'
else:
    theOS = '/'
    ecode = 'utf-8'

myfont = FontProperties(fname='tools'+ theOS + 'msj.ttf')

#讀取原始檔案
test_comments = pd.read_csv('data' + theOS + '蝦皮_運動內衣_留言資料.csv',encoding = ecode, engine= 'python')
test_contents = pd.read_csv('data' + theOS + '蝦皮_運動內衣_商品資料.csv',encoding = ecode, engine= 'python')

shopee_eda_instance = ShopeeEDA(test_comments,test_contents,myfont)
shopee_eda_instance.do_eda()

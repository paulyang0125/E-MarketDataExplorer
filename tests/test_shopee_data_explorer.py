#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""test"""

# tests/test_shopee_data_explorer.py

#from ast import keyword
import os
from typer.testing import CliRunner
import pytest
from emarket_data_explorer import (
    __app_name__,
    __version__,
    SUCCESS,
    ALL,
    PRODUCT_COMMENTS,
    PRODUCT_ITEMS,
    SHOPEE,
    DATA_SOURCES,
    cli,
    shopee_data_explorer,
    shopee_crawler,
    database,
    config,
)

runner = CliRunner()


def test_version():
    """ validate the --version output"""
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_init_over_cli() -> None:
    """test"""
    newline = "\n"
    result = runner.invoke(cli.app, ["init"], input='\n'.join([newline,newline]))
    assert result.exit_code == 0
    print(result.output)

test_data1 = {
    "keyword": "籃球鞋",
    "ip_addresses": shopee_crawler.DEFAULT_IP_RANGES,
    "proxy_auth": shopee_crawler.DEFAULT_PROXY_AUTH,
    "header": shopee_crawler.DEFAULT_HEADER,
    "path": shopee_crawler.DEFAULT_CHROME_WEBDRIVER,
    "page_num": 1,
    # "page_length":10,
    "read_index": {
        "keyword": "籃球鞋",
        "page_num": 1,
        # "page_length":10,
        "obtained_index_num": 5,
    }
}

test_data2 = {
    "keyword": "運動內衣",
    "ip_addresses": shopee_crawler.DEFAULT_IP_RANGES,
    "proxy_auth": shopee_crawler.DEFAULT_PROXY_AUTH,
    "header": shopee_crawler.DEFAULT_HEADER,
    "webdriver_path": shopee_crawler.DEFAULT_CHROME_WEBDRIVER,
    "page_num": 2,
    "page_length": 5,
    "read_index": {
        "keyword": "運動內衣",
        "page_num": 2,
        "page_length": 5,
        "obtained_index_num": 10
    }
}

'''
@pytest.mark.parametrize(
 "keyword,ip_addresses,proxy_auth,header,webdriver_path,page_num,page_length,expected",
    [
        pytest.param(
            test_data2["keyword"],
            test_data2["ip_addresses"],
            test_data2["proxy_auth"],
            test_data2["header"],
            test_data2["webdriver_path"],
            test_data2["page_num"],
            test_data2["page_length"],
            (test_data2["read_index"],SUCCESS)
        ),

    ]
)

'''


@pytest.mark.parametrize(
    "keyword,page_num,page_length,data_source, expected",
    [
        pytest.param(
            test_data2["keyword"],
            test_data2["page_num"],
            test_data2["page_length"],
            SHOPEE,
             (test_data2["read_index"], SUCCESS),
        ),

    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_read_index_api(keyword, page_num, page_length, data_source,expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
         database.DEFAULT_DB_FILE_PATH,\
        shopee_crawler.DEFAULT_IP_RANGES,\
         shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
              shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                  data_source)
    print("==expected: " + str(expected))
    actual = explorer.read_index_api(keyword, page_num, page_length)
    print("==actual: ", str(actual))
    assert actual == expected


@pytest.mark.parametrize(
    "keyword,page_num,data_source,expected",
    [
        pytest.param(
            test_data1["keyword"],
            test_data1["page_num"],
            SHOPEE,
            (test_data1["read_index"], SUCCESS)
        ),

    ]
)

@pytest.mark.skip(reason="since this test takes long time, skip first until v1.3 starts")
def test_read_index_selenium(keyword, page_num, data_source, expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
        shopee_crawler.DEFAULT_IP_RANGES, \
        shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
             shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                 data_source)
    print("==expected: " + str(expected))
    actual = explorer.read_index_selenium(keyword, page_num)
    print("==actual: ", str(actual))
    assert actual == expected

@pytest.mark.parametrize(
    "keyword,page_num,page_length,data_source,expected",
    [
        pytest.param(
            test_data2["keyword"],
            test_data2["page_num"],
            test_data2["page_length"],
            SHOPEE,
            test_data2["page_num"] * test_data2["page_length"],
        ),

    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_read_index(keyword, page_num, page_length, data_source, expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
        shopee_crawler.DEFAULT_IP_RANGES,\
         shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
              shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                  data_source)

    actual = explorer.read_index(keyword,page_num,page_length)
    assert actual.error == 0
    assert len(actual.scraping_info) == expected


test_data3 = {
    "item_id": 16439834350,"shop_id":555952616
}

test_data4 = {
    "item_id": 9488303342,"shop_id":267479790
}

@pytest.mark.parametrize(
    "shop_id,item_id,data_source,expected",
        [
        pytest.param(
            test_data3["shop_id"],
            test_data3["item_id"],
            SHOPEE,
            test_data3["item_id"],
        ),
        pytest.param(
            test_data4["shop_id"],
            test_data4["item_id"],
            SHOPEE,
            test_data4["item_id"],
        ),


    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_read_good_details(shop_id, item_id, data_source, expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
        shopee_crawler.DEFAULT_IP_RANGES,\
         shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
              shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                  data_source)
    actual = explorer.read_good_details(shop_id=shop_id, item_id=item_id)
    #print("test_read_good_details: autual - " , str(actual))
    assert actual.error == 0
    #assert actual.scraping_info['description']
    assert actual.scraping_info['item']['itemid'] == expected

@pytest.mark.parametrize(
    "shop_id,item_id,data_source,expected",
        [
        pytest.param(
            test_data3["shop_id"],
            test_data3["item_id"],
            SHOPEE,
            test_data3["item_id"],
        ),
        pytest.param(
            test_data4["shop_id"],
            test_data4["item_id"],
            SHOPEE,
            test_data4["item_id"],
        ),


    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_read_good_comments(shop_id, item_id, data_source,expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
        shopee_crawler.DEFAULT_IP_RANGES,\
         shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
              shopee_crawler.DEFAULT_CHROME_WEBDRIVER,data_source)
    actual = explorer.read_good_comments(shop_id=shop_id, item_id=item_id)

    #print("test_read_good_comments: actual - " , str(actual))
    assert actual.error == 0
    #assert actual.scraping_info['product_items']
    assert actual.scraping_info[0]['itemid'] == expected

@pytest.mark.parametrize(
    "keyword,num_of_product,mode,page_length,data_source,expected",
    [
        pytest.param(
            test_data2["keyword"],
            20,
            ALL,
            10,
            SHOPEE,
            20,
        ),
        pytest.param(
            test_data2["keyword"],
            20,
            PRODUCT_ITEMS,
            10,
            SHOPEE,
            20,
        ),
        pytest.param(
            test_data2["keyword"],
            10,
            PRODUCT_COMMENTS,
            10,
            SHOPEE,
            10,
        ),

    ]
)

#shopee_data_explorer.Explorer(data_path,db_path,ip_addresses,proxy_auth,my_header,\
#            webdriver_path, int(data_source))

@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap(keyword, num_of_product, mode,page_length, data_source, expected):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
    shopee_crawler.DEFAULT_IP_RANGES,\
        shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
            shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                data_source)
    actual = explorer.scrap(keyword=keyword, num_of_product=num_of_product,mode=mode,\
        page_length=page_length)
    assert actual.error == 0
    if mode != PRODUCT_COMMENTS:
        assert actual.scraping_info["obtained_product_num"] == expected
    else:
        assert actual.scraping_info["obtained_comment_num"] >= expected

@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_over_cli():
    """ validate the scrap cli output"""
    result = runner.invoke(cli.app, ["scrap","運動內衣","50","50"])
    assert result.exit_code == 0
    print(result.stdout)
    assert "運動內衣" and "50" in result.stdout

@pytest.mark.parametrize(
    "product_comment_name,product_csv_name,data_source",
    [
        pytest.param(
            "shopee_運動內衣_product_comments.csv",
            "shopee_運動內衣_product_goods.csv",
            SHOPEE,

        ),
        pytest.param(
            "shopee_男性皮夾_product_comments.csv",
            "shopee_男性皮夾_product_goods.csv",
            SHOPEE,

        ),

    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_do_eda(product_csv_name,product_comment_name, data_source):
    """test"""
    explorer = shopee_data_explorer.Explorer(shopee_crawler.DEFAULT_DATA_PATH, \
        database.DEFAULT_DB_FILE_PATH,\
    shopee_crawler.DEFAULT_IP_RANGES,\
        shopee_crawler.DEFAULT_PROXY_AUTH,shopee_crawler.DEFAULT_HEADER,\
            shopee_crawler.DEFAULT_CHROME_WEBDRIVER,\
                data_source)
    result, error = explorer.do_eda(product_csv_name,product_comment_name)
    assert error == 0
    print("result: ", result)
    assert len(result) == 0

@pytest.mark.parametrize(
    "product_comment_name,product_csv_name,data_source",
    [
        pytest.param(
            "shopee_運動內衣_product_comments.csv",
            "shopee_運動內衣_product_goods.csv",
            SHOPEE,

        ),
        pytest.param(
            "shopee_男性皮夾_product_comments.csv",
            "shopee_男性皮夾_product_goods.csv",
            SHOPEE,

        ),

    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_eda_over_cli(product_csv_name,product_comment_name,data_source):
    """ validate the eda cli output"""
    result = runner.invoke(cli.app, ["eda",product_csv_name,\
         product_comment_name])
    #if config.CONFIG_FILE_PATH.exists():
    data_path= shopee_crawler.get_data_path(config.CONFIG_FILE_PATH)
    assert result.exit_code == 0
    assert data_path.joinpath("figure1.png").exists()
    assert data_path.joinpath("figure2.png").exists()
    assert data_path.joinpath("figure3.png").exists()
    assert data_path.joinpath("figure4.png").exists()
    assert data_path.joinpath("figure5.png").exists()
    assert data_path.joinpath("figure6.png").exists()
    assert data_path.joinpath(f"{DATA_SOURCES[data_source]}_eda_report.html").exists()


@pytest.mark.parametrize(
    "keyword,page_num,page_length",
    [
        pytest.param(
            test_data2["keyword"],
            test_data2["page_num"],
            test_data2["page_length"],

        ),

    ]
)
# todo: somehow assert result.exit_code == 0 reports failed and also complain int call len()
@pytest.mark.skip(reason="tested, skip first to save time")
def test_read_search_over_cli(keyword,page_num,page_length) -> None:
    "test"
    result = runner.invoke(cli.app, ["read-search",keyword,page_num,page_length, '--searcher_type',1])
    print(result.exit_code)
    print(type(result.exit_code))
    #assert result.exit_code == 0
    print(result.output)
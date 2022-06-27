#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 26/06/2022
# version ='1.3.1'
# ---------------------------------------------------------------------------

"""pytest for unit test and acceptance test"""

# tests/test_shopee_data_explorer.py

#from ast import keyword
from typer.testing import CliRunner
import pytest
from emarket_data_explorer import (
    __app_name__,
    __version__,
    SUCCESS,
    ALL,
    PRODUCT_INDEXES,
    PRODUCT_ITEMS,
    PRODUCT_COMMENTS,
    # PRODUCT_ITEMS,
    SHOPEE,
    DATA_SOURCES,
    cli,
    shopee_data_explorer,
    constant,
    shopee_crawler,
    config,
)

runner = CliRunner()

def get_explorer(data_source):
    """test"""
    return shopee_data_explorer.ShopeeExplorer(data_path=constant.DEFAULT_DATA_PATH, \
         db_path=constant.DEFAULT_DB_FILE_PATH,\
        ip_addresses=constant.DEFAULT_IP_RANGES,\
         proxy_auth=constant.DEFAULT_PROXY_AUTH,my_header=constant.DEFAULT_HEADER,\
              webdriver_path=constant.DEFAULT_CHROME_WEBDRIVER,\
                  data_source=data_source)

def test_version():
    """ validate the --version output"""
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_init_over_cli() -> None:
    """test"""
    newline = "\n"
    result = runner.invoke(cli.app, ["init"], input='\n'.join([newline]))
    assert result.exit_code == 0
    print(result.output)

############# test parameters ##############



test_data1_1 = {
    "keyword": "籃球鞋",
    "num_of_product": 100,
    "page_length":50,
    "mode":ALL,
    "data_source":SHOPEE,
}

test_data1_2 = {
    "keyword": "籃球鞋",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_ITEMS,
    "data_source":SHOPEE,
}

test_data1_3 = {
    "keyword": "籃球鞋",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_COMMENTS,
    "data_source":SHOPEE,
}

test_data1_4 = {
    "keyword": "籃球鞋",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_INDEXES,
    "data_source":SHOPEE,
}
test_data2_1 = {
    "keyword": "運動內衣",
    "num_of_product": 50,
    "page_length":50,
    "mode":ALL,
    "data_source":SHOPEE,
}

test_data2_2 = {
    "keyword": "運動內衣",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_ITEMS,
    "data_source":SHOPEE,
}

test_data2_3 = {
    "keyword": "運動內衣",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_COMMENTS,
    "data_source":SHOPEE,
}

test_data2_4 = {
    "keyword": "運動內衣",
    "num_of_product": 100,
    "page_length":50,
    "mode":PRODUCT_INDEXES,
    "data_source":SHOPEE,
}

test_data3_1 = {
    "keyword": "男性皮夾",
    "num_of_product": 100,
    "page_length":50,
    "mode":ALL,
    "data_source":SHOPEE,
}




############# scrap ##############



@pytest.mark.parametrize(
    #"keyword,num_of_product,mode,page_length,data_source,expected",
    "keyword,num_of_product,mode,page_length,data_source",
    [
        pytest.param(
            test_data1_1["keyword"],
            test_data1_1["num_of_product"],
            test_data1_1["mode"],
            test_data1_1["page_length"],
            test_data1_1["data_source"],
            #test_data1_1["num_of_product"],
        ),

        pytest.param(
            test_data2_1["keyword"],
            test_data2_1["num_of_product"],
            test_data2_1["mode"],
            test_data2_1["page_length"],
            test_data2_1["data_source"],
            #test_data2_1["num_of_product"],
        ),

    ]
)


@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_async(keyword, num_of_product, mode, page_length, data_source):
    """test"""
    explorer = get_explorer(data_source)
    result = explorer.scrap_async(keyword=keyword, num_of_product=num_of_product,mode=mode,\
        page_length=page_length)
    print(result[1])
    assert SUCCESS in result[1]






@pytest.mark.parametrize(
    #"keyword,num_of_product,mode,page_length,data_source,expected",
    "keyword,num_of_product,mode,page_length",
    [
        pytest.param(
            test_data3_1["keyword"],
            str(test_data3_1["num_of_product"]),
            test_data3_1["mode"],
            str(test_data3_1["page_length"]),
        ),

    ]
)


@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_async_all_over_cli(keyword,num_of_product,page_length,mode) -> None:
    "test"
    #result = runner.invoke(cli.app, ["scrap-async",keyword,page_num, '-ve', 1])
    result = runner.invoke(cli.app, ["scrap-async",keyword,num_of_product,'-sm', mode])
    #result = runner.invoke(cli.app, ["scrap-async","運動內衣","100","50"])
    print(result.exit_code)
    print(type(result.exit_code))
    #assert result.exit_code == 0
    print(result.stdout)
    print(type(result.stdout))
    #sample stdout: explorer: "運動內衣" was searched and collected \
    # successfully with options: page_num 100 and page_length 50
    assert keyword and num_of_product and page_length in result.stdout




@pytest.mark.parametrize(
    #"keyword,num_of_product,mode,page_length,data_source,expected",
    "keyword,num_of_product,mode,page_length",
    [
        pytest.param(
            test_data1_2["keyword"],
            str(test_data1_2["num_of_product"]),
            test_data1_2["mode"],
            str(test_data1_2["page_length"]),
        ),

    ]
)


@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_async_product_over_cli(keyword,num_of_product,page_length,mode) -> None:
    "test"

    result = runner.invoke(cli.app, ["scrap-async",keyword,num_of_product,page_length,'-sm', mode])
    print(result.exit_code)
    print(type(result.exit_code))
    #assert result.exit_code == 0
    print(result.stdout)
    print(type(result.stdout))
    #sample stdout: explorer: "運動內衣" was searched and collected \
    # successfully with options: page_num 100 and page_length 50
    assert keyword and num_of_product and page_length in result.stdout


@pytest.mark.parametrize(
    "keyword,num_of_product,mode,page_length",
    [
        pytest.param(
            test_data1_3["keyword"],
            str(test_data1_3["num_of_product"]),
            test_data1_3["mode"],
            str(test_data1_3["page_length"]),
        ),

    ]
)


@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_async_comment_over_cli(keyword,num_of_product,page_length, mode) -> None:
    "test"

    result = runner.invoke(cli.app, ["scrap-async",keyword,num_of_product,\
        page_length,'--scrap_mode_for_shopee', mode])
    print(result.exit_code)
    print(type(result.exit_code))
    #assert result.exit_code == 0
    print(result.stdout)
    print(type(result.stdout))
    #sample stdout: explorer: "運動內衣" was searched and collected successfully \
    # with options: page_num 100 and page_length                 50
    assert keyword and num_of_product and page_length in result.stdout


@pytest.mark.parametrize(
    "keyword,num_of_product,mode,page_length",
    [
        pytest.param(
            test_data1_4["keyword"],
            str(test_data1_4["num_of_product"]),
            test_data1_4["mode"],
            str(test_data1_4["page_length"]),
        ),

    ]
)

@pytest.mark.skip(reason="tested, skip first to save time")
def test_scrap_async_index_over_cli(keyword,num_of_product,page_length,mode) -> None:
    "test"
    result = runner.invoke(cli.app, ["scrap-async",keyword,num_of_product,page_length,\
        '--scrap_mode_for_shopee', mode])
    print(result.exit_code)
    print(type(result.exit_code))
    #assert result.exit_code == 0
    print(result.stdout)
    print(type(result.stdout))
    #sample stdout: explorer: "運動內衣" was searched and collected successfully with \
    # options: page_num 100 and page_length                 50
    assert keyword and num_of_product and page_length in result.stdout



############  eda ################

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
    explorer = get_explorer(data_source)
    result, error = explorer.do_eda(product_csv_name,product_comment_name)
    assert error == 0
    print("result: ", result)
    assert len(result) == 0

@pytest.mark.parametrize(
    "product_comment_name,product_csv_name,data_source",
    [
        pytest.param(
            "shopee_籃球鞋_product_comments.csv",
            "shopee_籃球鞋_product_goods.csv",
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

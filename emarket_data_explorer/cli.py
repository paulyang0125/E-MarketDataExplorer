#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 26/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the E-market Data Explorer CLI.


Todo:\n
1. will move init_data job to config.py or data_builder.py in v1.4\n
2. will implement retry by adding the abstract class to decouple the retry mechanism in v1.4\n
3. to standardized the typer.exit code, define scrap-async error code in v1.4

"""

# emarket_data_explorer/cli.py

import logging
import sys
from pathlib import Path
from typing import Dict, List
from typing import Optional

import typer
from emarket_data_explorer import (
    SUCCESS, ERRORS, __app_name__, __version__, config, database, \
        constant, shopee_crawler, shopee_data_explorer
)


app = typer.Typer()
#self, ip_addresses: List[str], proxy_auth: str, header: Dict[str, any],path:str
@app.command()
def init(
    data_path: str = typer.Option(
        str(constant.DEFAULT_DATA_PATH),
        "--data-path",
        "-data",
        prompt="e-market data explorer data location?",
        help="where e-market data explorer will save its finding on your OS",
    ),
    data_source: int = typer.Option(
        1, "--data_source", "-d", min=1, max=3,
        prompt="e-market data explorer data source?",
        help="1 indicates you will scrap Shopee, 2 is for PPT and 3 stands for Amazon",
    ),

) -> None:
    """
    Initialize the shopee explorer data folder.
    """
    db_path = str(database.DEFAULT_DB_FILE_PATH)
    ip_addresses = str(constant.DEFAULT_IP_RANGES)
    proxy_auth = str(constant.DEFAULT_PROXY_AUTH)
    my_header = constant.DEFAULT_HEADER #it's a dict
    webdriver_path = constant.DEFAULT_CHROME_WEBDRIVER


    app_init_error,config_file_path = config.init_app(data_path=data_path, \
        ip_addresses=ip_addresses, proxy_auth=proxy_auth,my_header=my_header, \
            webdriver_path=webdriver_path,data_source=data_source,db_path=db_path)

    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer config is {config_file_path}", fg=typer.colors.GREEN)

    #todo: will move init_data job to config.py or data_builder.py in v1.4
    data_init_error = shopee_crawler.init_data(Path(data_path))

    if data_init_error:
        typer.secho(
            f'Creating shopee explorer data failed with "{ERRORS[data_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer data is {data_path}", fg=typer.colors.GREEN)

def get_explorer() -> shopee_data_explorer.ShopeeExplorer:
    """reads data in configs and passes them as args to initialize
    shopee_data_explorer.Explorer class

    Args:
        None

    Returns:
        the instance of shopee_data_explorer.Explorer


    """

    #def __init__(self,data_path:Path,ip_addresses: List[str], proxy_auth: str, \
    #header: Dict[str, any], webdriver_path:str) -> None:
    if config.CONFIG_FILE_PATH.exists():
        #data_path = constant.get_data_path(config.CONFIG_FILE_PATH)
        data_path,ip_addresses,proxy_auth,webdriver_path,data_source,db_path,my_header = \
            shopee_crawler.get_configs_data(config.CONFIG_FILE_PATH)
        if not data_path.exists():
            typer.secho(
                        'Config file error. Please, run "shopee_data_explorer\
                                init"',
                        fg=typer.colors.RED,
                    )
            raise typer.Exit(1)
        if not isinstance(ip_addresses, List):
            typer.secho(
                        'ip_addresses in Config file error. Please, \
                            run "shopee_data_explorer\
                                init"',
                        fg=typer.colors.RED,
                    )
            raise typer.Exit(1)
        if not proxy_auth and not webdriver_path:
            typer.secho(
                        'proxy_auth or webdriver path in Config file error. Please, \
                            run "shopee_data_explorer\
                                init"',
                        fg=typer.colors.RED,
                    )
            raise typer.Exit(1)
        if not isinstance(my_header,Dict):
            typer.secho(
                        'my_header in Config file error. Please, \
                            run "shopee_data_explorer\
                                init"',
                        fg=typer.colors.RED,
                    )
            raise typer.Exit(1)
        if not data_source:
            typer.secho(
                        'data_source in Config file error. Please, \
                            run "shopee_data_explorer\
                                init"',
                        fg=typer.colors.RED,
                    )
            raise typer.Exit(1)

    else:
        typer.secho(
            'Config file not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # if data_path.exists() and isinstance(ip_addresses, List) and proxy_auth \
    #     and webdriver_path and isinstance(my_header,Dict) and data_source:
    return shopee_data_explorer.ShopeeExplorer(data_path=data_path,db_path=db_path,\
        ip_addresses=ip_addresses,proxy_auth=proxy_auth,my_header=my_header, \
            webdriver_path=webdriver_path, data_source=int(data_source))

    # else:
    #     typer.secho(
    #         'the config arguments data not found. Please, run "shopee_data_explorer init"',
    #         fg=typer.colors.RED,
    #     )
    #     raise typer.Exit(1)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

### remove ###


### remove ###

@app.command()
#input arg -> file1: csv, file2: csv

def eda(
    required_args :List[str] = typer.Argument(
        ...,
        help=
        """
            here expects two arguments in sequence\n
            1. the scraped CSV name xxx_YOUR_KEYWORD_product_goods.csv\n
            2. another scraped CSV name xxx_YOUR_KEYWORD_product_comments.csv.\n
            For example, e-market-data-explorer eda file1 file2.
        """
            ,
        ),

) -> None:
    """
    Create EDA process and charts from csv files

    """
    # debug
    #print(f'inputs are args - {required_args}')
    if len(required_args) != 2:
        typer.secho(
        f'{required_args} are invalid for type1 searcher', fg=typer.colors.RED
    )
        raise typer.Exit(1)
    products_csv_name = required_args[0]
    comment_csv_name = required_args[1]
    explorer = get_explorer()
    response, error = explorer.do_eda(products_csv_name,comment_csv_name)
    if error:
        typer.secho(
            f'failed with "{ERRORS[error]}"'\
                f"""errors are {response}"""
                , fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""eda for {products_csv_name} and {comment_csv_name} completes successfully"""
            f"""go to data folder to see the results""",
            fg=typer.colors.GREEN,
        )

### remove ###



### remove ###


@app.command()
#input arg -> keyword: str, num of product: int, page_length: int (optional),
#DEFAULT_PAGE_LENGTH = 10
def scrap_async(
    required_args :List[str] = typer.Argument(
        ...,
        help=
        """
        Here expects three inputs in sequence\n
        1. keyword you want to search for\n
        2. the number of product\n
        3. the length of page (optional)\n
        For example, e-market-data explorer scrap basketball 100
        """,
        ),
    mode: int = typer.Option(
        1, "--scrap_mode_for_shopee", "-sm", min=1, max=4,
        help="we have three modes ALL, PRODUCT_ITEMS, PRODUCT_COMMENTS available. user can \
choose to scrap all two data (product or comment or index) or three for ALL. the default is 1 for ALL."
        ),
    verbose_level: int = typer.Option(
        3, "--verbose", "-ve", min=1, max=3,
        help="verbose 1 dumps all detailed debugging info, the default 3 just print \
error message if something bad happens."
        )
) -> None:
    """
    Scrap commercial data from the data source specified by user

    """
    if verbose_level == 1:
        logging.basicConfig(format='%(asctime)s %(message)s',stream=sys.stdout,\
            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    elif verbose_level == 2:
        logging.basicConfig(format='%(asctime)s %(message)s',stream=sys.stdout,\
            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    elif verbose_level == 3:
        logging.basicConfig(format='%(asctime)s %(message)s',stream=sys.stdout,\
            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.FATAL)


    mylogger = logging.getLogger(__name__)


    # debug
    #mylogger.debug(f'inputs are args - {required_args}, mode - {mode}, searcher-type - \
    #    {searcher_type}, retry - {retry}')
    retry = 3
    mylogger.debug('inputs are args - %s, mode - %i,\
         retry - %i, verbose - %i', required_args, mode,\
            retry, verbose_level)

    if len(required_args) < 2:
        typer.secho(
        f'{required_args} are invalid for type1 searcher', fg=typer.colors.RED
    )
        raise typer.Exit(1)
    else:
        keyword = required_args[0]
        num_of_product = int(required_args[1])
        #if num_of_product < 10, or default one (now is 10)
        # need to fill the minimum to at least default
        #if num_of_product
        if num_of_product < constant.DEFAULT_PAGE_LENGTH:
            num_of_product = constant.DEFAULT_PAGE_LENGTH

        # we limit the number of item to be scraped.
        if num_of_product > 100:
            num_of_product = 100


        try:
            if required_args[2]:
                page_length = int(required_args[2])
        except IndexError:
            page_length = constant.DEFAULT_PAGE_LENGTH_ASYNC
            typer.secho(f'page_length is not given,'
                        f'the app will use default length:{constant.DEFAULT_PAGE_LENGTH}'
                        , fg=typer.colors.YELLOW)

        typer.secho(
                f"""scrap for {keyword} is starting!""",
                fg=typer.colors.GREEN,
            )

        explorer = get_explorer()
        result = explorer.scrap_async(keyword,num_of_product,mode,page_length)


        #if mode == 1:
        if not SUCCESS in result[1]:
            typer.secho(
            #     f'failed with "{ERRORS[error]}"', fg=typer.colors.RED
            # )
            # raise typer.Exit(error)
                f'failed with "{str(result[1])}"', fg=typer.colors.RED
            )
            #raise typer.Exit(error)
            #todo: to standardized the typer.exit code, define scrap-async error code,
            # will do in v1.4
            raise typer.Exit(15)
        else:
            if mode == 1:
                typer.secho(
                    f"""explorer: "{keyword}" was searched and collected successfully\n"""
                    f"""with options: page_num {num_of_product} and page_length {page_length} \n"""
                    f"""obtained_index_num: {result[0]["obtained_index_num"]} \n"""
                    f"""obtained_good_num: {result[0]["obtained_good_num"]} \n"""
                    f"""obtained_comment_num: {result[0]["obtained_comment_num"]} \n""",
                    fg=typer.colors.GREEN,
                )
            if mode == 2:
                typer.secho(
                    f"""explorer: "{keyword}" was searched and collected successfully\n"""
                    f"""with options: page_num {num_of_product} and page_length {page_length} \n"""
                    f"""obtained_index_num: {result[0]["obtained_index_num"]} \n"""
                    f"""obtained_good_num: {result[0]["obtained_good_num"]} \n""",
                    fg=typer.colors.GREEN,
                )
            if mode == 3:
                typer.secho(
                    f"""explorer: "{keyword}" was searched and collected successfully\n"""
                    f"""with options: page_num {num_of_product} and page_length {page_length} \n"""
                    f"""obtained_index_num: {result[0]["obtained_index_num"]} \n"""
                    f"""obtained_comment_num: {result[0]["obtained_comment_num"]} \n""",
                    fg=typer.colors.GREEN,
                )
            if mode == 4:
                typer.secho(
                    f"""explorer: "{keyword}" was searched and collected successfully\n"""
                    f"""with options: page_num {num_of_product} and page_length {page_length} \n"""
                    f"""obtained_index_num: {result[0]["obtained_index_num"]} \n """,
                    fg=typer.colors.GREEN,
                )



            # scraper_response = {
            #             "ids_pool":result[0],
            #             "obtained_index_num":len(result[1].index),
            #             "obtained_good_num":len(result[2].index),
            #             "obtained_comment_num":len(result[3].index),
            #         }




@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """
    E-Market Data Explorer is a Python-based crawler and exploratory data analysis(EDA) tool
    for marketing specialties who would like to conduct the STP methods for working out
    their marketing strategy for sale and promotion.

    Updated for E-Market Data Explorer 1.1, June 2022

    Author:

    Currently written and maintained by Paul Yang <paulyang0125@gmail> and \
Kana Kunikata <vinaknkt@gmail.com>.

    """
    typer.secho(f"""{version}""",fg=typer.colors.GREEN)
    return

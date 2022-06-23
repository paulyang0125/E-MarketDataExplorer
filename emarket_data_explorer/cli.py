#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the E-market Data Explorer CLI.


Todo at v1.3:\n
1. will move init_data job to config.py or data_builder.py in v1.3+\n
2. will implement retry by adding the abstract class to decouple the retry mechanism


"""

# emarket_data_explorer/cli.py

import logging
import sys
from pathlib import Path
from typing import Dict, List
from typing import Optional

import typer
from emarket_data_explorer import (
    SUCCESS, ERRORS, __app_name__, __version__, database, config, shopee_crawler, shopee_data_explorer
)

app = typer.Typer()
#self, ip_addresses: List[str], proxy_auth: str, header: Dict[str, any],path:str
@app.command()
def init(
    data_path: str = typer.Option(
        str(shopee_crawler.DEFAULT_DATA_PATH),
        "--data-path",
        "-data",
        prompt="e-market data explorer data location?",
        help="where e-market data explorer will save its finding on your OS",
    ),
    #  db_path: str = typer.Option(
    #     str(database.DEFAULT_DB_FILE_PATH),
    #     "--db-path",
    #     "-db",
    #     prompt="e-market data database location?",
    #     help="where e-market data explorer will save the index database on your OS",
    # ),
    # ip_addresses: str = typer.Option(
    #     str(shopee_crawler.DEFAULT_IP_RANGES),
    #     "--ips-range",
    #     "-ips",
    #     prompt="e-market data explorer proxy ip ranges?",
    #     help="e-market data explorer will rotate its IP based on those proxy IP addresses",
    # ),

    # proxy_auth: str = typer.Option(
    #     str(shopee_crawler.DEFAULT_PROXY_AUTH),
    #     "--proxy-auth",
    #     "-proxy",
    #     prompt="e-market data explorer proxy credential?",
    #     help="e-market data explorer will access the proxy server based on this credential",
    # ),
    #my_header: str = typer.Option(
    #    str(shopee_crawler.DEFAULT_HEADER),
    #    "--myheader",
    #    "-header",
    #    prompt="shopee explorer http/https header?",
    #),

    # webdriver_path: str = typer.Option(
    #     str(shopee_crawler.DEFAULT_CHROME_WEBDRIVER),
    #     "--webdriver-path",
    #     "-webdriver",
    #     prompt="e-market data explorer webdriver path?",
    #     help="this is where you store the selenium webdriver. currently we can support Chrome",
    # ),

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
    ip_addresses = str(shopee_crawler.DEFAULT_IP_RANGES)
    proxy_auth = str(shopee_crawler.DEFAULT_PROXY_AUTH)
    my_header = shopee_crawler.DEFAULT_HEADER #it's a dict
    webdriver_path = shopee_crawler.DEFAULT_CHROME_WEBDRIVER


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

    #todo: will move init_data job to config.py or data_builder.py in v1.3+
    data_init_error = shopee_crawler.init_data(Path(data_path))

    if data_init_error:
        typer.secho(
            f'Creating shopee explorer data failed with "{ERRORS[data_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer data is {data_path}", fg=typer.colors.GREEN)

def get_explorer() -> shopee_data_explorer.Explorer:
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
        #data_path = shopee_crawler.get_data_path(config.CONFIG_FILE_PATH)
        data_path,ip_addresses,proxy_auth,webdriver_path,data_source,db_path,my_header = \
            shopee_crawler.get_configs_data(config.CONFIG_FILE_PATH)

    else:
        typer.secho(
            'Config file not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if data_path.exists() and isinstance(ip_addresses, List) and proxy_auth \
        and webdriver_path and isinstance(my_header,Dict) and data_source:
        return shopee_data_explorer.Explorer(data_path=data_path,db_path=db_path,\
            ip_addresses=ip_addresses,proxy_auth=proxy_auth,my_header=my_header, \
                webdriver_path=webdriver_path, data_source=int(data_source))
    else:
        typer.secho(
            'the config arguments data not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
#input arg -> keyword: str, page_num: int,page_length

def read_search(
    required_args :List[str] = typer.Argument(
        ...,
        help=
        """
        Here expects three arguments in sequence \n
        1. keyword you want to search for \n
        2. the number of page \n
        3. the length of page \n
        The total amount of item to be searched equals
        the multiplication of the second argument and the third.
        """
        ),
        searcher_type: int = typer.Option(
        1, "--searcher_type", "-t", min=1, max=2,
        help="the default is 1 meaning e-market explorer will scrap data over \
data source API and choosing 2 will use selenium to scrap shopee website",
        ),
    # todo: will implement retry by adding the abstract class to decouple the retry mechanism
    #retry: int = typer.Option(1, "--retry", "-r", min=1, max=5),
) -> None:
    """
    Reads search data from shopee (for debugging). This belongs to \
the debugging feature which will only read the search results as the index.

    """

    #print(f'inputs are {required_args}, {searcher_type}, {retry}')
    if searcher_type == 1:
        if len(required_args) != 3:
            typer.secho(
            f'{required_args} are invalid for type1 searcher', fg=typer.colors.RED
        )
            raise typer.Exit(2)
        else:
            keyword = required_args[0]
            page_num = int(required_args[1])
            page_length = int(required_args[2])
            explorer = get_explorer()
            response, error = explorer.read_index_api(keyword,page_num,page_length)
            if error:
                typer.secho(
                    f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
                )
                raise typer.Exit(5)
            else:
                typer.secho(
                    f"""explorer: "{response['keyword']}" was searched """
                    f"""with options: page_num {response['page_num']} and page_length \
                        {response['page_length']} """
                    f"""finally it obtains the number of search result: \
                        {response['obtained_index_num']} """,
                    fg=typer.colors.GREEN,
                )

    elif searcher_type == 2:
        if len(required_args) != 2:
            typer.secho(
            f'{required_args} are invalid for type2 searcher', fg=typer.colors.RED
        )
            raise typer.Exit(1)
        else:
            keyword = required_args[0]
            page_num = int(required_args[1])
            explorer = get_explorer()
            response, error = explorer.read_index_selenium(keyword,page_num)
            if error:
                typer.secho(
                    f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
                )
                raise typer.Exit(1)
            else:
                typer.secho(
                    f"""explorer: "{response['keyword']}" was searched """
                    f"""with options: page_num {response['page_num']} """
                    f"""finally it obtains the number of search result: \
                        {response['obtained_index_num']} """,
                    fg=typer.colors.GREEN,
                )



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


@app.command()
#input arg -> keyword: str, num of product: int, page_length: int (optional),
#DEFAULT_PAGE_LENGTH = 10
def scrap(
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
    #source: int = typer.Option(0, "--scrap_source", "-ss", min=0, max=2),
    mode: int = typer.Option(
        1, "--scrap_mode_for_shopee", "-sm", min=1, max=3,
        help="we have three modes ALL, PRODUCT_ITEMS, PRODUCT_COMMENTS available. user can \
choose to scrap all two data (product or comment) or both for ALL. the default is 1 for ALL."
        ),
    searcher_type: int = typer.Option(
        1, "--searcher_type", "-st", min=1, max=2,
        help="he default is 1 meaning e-market explorer will scrap data over \
Shopee API and choosing another 2 will use selenium to scrap shopee website."
        ),
    retry: int = typer.Option(
        1, "--retry", "-r", min=1, max=5,
        help="this is not yet supported, we'll target v1.3 to implement."
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

    mylogger.debug('inputs are args - %s, mode - %i, searcher-type - \
        %i, retry - %i, verbose - %i', required_args, mode, searcher_type, retry, verbose_level)

    if searcher_type == 1:
        if len(required_args) < 2:
            typer.secho(
            f'{required_args} are invalid for type1 searcher', fg=typer.colors.RED
        )
            raise typer.Exit(1)
        else:
            keyword = required_args[0]
            num_of_product = int(required_args[1])
            try:
                if required_args[2]:
                    page_length = int(required_args[2])
            except IndexError:
                page_length = shopee_crawler.DEFAULT_PAGE_LENGTH
                typer.secho(f'page_length is not given, the app will use default\
                     length:{shopee_crawler.DEFAULT_PAGE_LENGTH}', fg=typer.colors.YELLOW)

            typer.secho(
                    f"""scrap for {keyword} is starting!""",
                    fg=typer.colors.GREEN,
                )

            explorer = get_explorer()
            response, error = explorer.scrap(keyword,num_of_product,mode,page_length)
            if error:
                typer.secho(
                    f'failed with "{ERRORS[error]}"', fg=typer.colors.RED
                )
                raise typer.Exit(error)
            else:
                typer.secho(
                    f"""explorer: "{response['keyword']}" was searched"""
                    f"""and collected successfully\n"""
                    f"""with options: page_num {response['page_num']} and  """
                    f"""page_length {response['page_length']}\n""",
                    fg=typer.colors.GREEN,
                )
    else:
        typer.secho(
            "sorry, it's not supported yet. please wait for the next version",
             fg=typer.colors.RED,
        )
        raise typer.Exit(10)



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
    #source: int = typer.Option(0, "--scrap_source", "-ss", min=0, max=2),
    mode: int = typer.Option(
        1, "--scrap_mode_for_shopee", "-sm", min=1, max=4,
        help="we have three modes ALL, PRODUCT_ITEMS, PRODUCT_COMMENTS available. user can \
choose to scrap all two data (product or comment or index) or three for ALL. the default is 1 for ALL."
        ),
    retry: int = typer.Option(
        1, "--retry", "-r", min=1, max=5,
        help="this is not yet supported, we'll target v1.3 to implement."
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
        try:
            if required_args[2]:
                page_length = int(required_args[2])
        except IndexError:
            page_length = shopee_crawler.DEFAULT_PAGE_LENGTH
            typer.secho(f'page_length is not given, the app will use default\
                    length:{shopee_crawler.DEFAULT_PAGE_LENGTH}', fg=typer.colors.YELLOW)

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
            #todo: to standardlize the typer.exit code
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

    Currently written maintained by Paul Yang <paulyang0125@gmail> and \
Kana Kunikata <vinaknkt@gmail.com>.

    """
    typer.secho(f"""{version}""",fg=typer.colors.GREEN)
    return

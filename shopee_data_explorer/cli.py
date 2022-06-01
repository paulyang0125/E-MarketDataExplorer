#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Explorer CLI."""
# shopee_data_explorer/cli.py
from email import header
from typing import Any, Dict, List, NamedTuple
from pathlib import Path
from typing import Optional
import typing

import typer

from shopee_data_explorer import (
    ERRORS, __app_name__, __version__, config, shopee_crawler, shopee_data_explorer
)

app = typer.Typer()
#self, ip_addresses: List[str], proxy_auth: str, header: Dict[str, any],path:str
@app.command()
def init(
    data_path: str = typer.Option(
        str(shopee_crawler.DEFAULT_DATA_PATH),
        "--data-path",
        "-data",
        prompt="shopee explorer data location?",
    ),
    ip_addresses: str = typer.Option(
        str(shopee_crawler.DEFAULT_IP_RANGES),
        "--ips-range",
        "-ips",
        prompt="shopee explorer proxy ip ranges?",
    ),

    proxy_auth: str = typer.Option(
        str(shopee_crawler.DEFAULT_PROXY_AUTH),
        "--proxy-auth",
        "-proxy",
        prompt="shopee explorer proxy credential?",
    ),
    #my_header: str = typer.Option(
    #    str(shopee_crawler.DEFAULT_HEADER),
    #    "--myheader",
    #    "-header",
    #    prompt="shopee explorer http/https header?",
    #),

    webdriver_path: str = typer.Option(
        str(shopee_crawler.DEFAULT_CHROME_WEBDRIVER),
        "--webdriver-path",
        "-webdriver",
        prompt="shopee explorer webdriver path?",
    ),

) -> None:
    """Initialize the shopee explorer data folder."""
    app_init_error,config_file_path = config.init_app(data_path=data_path, \
        ip_addresses=ip_addresses, proxy_auth=proxy_auth,my_header=shopee_crawler.DEFAULT_HEADER, \
            webdriver_path=webdriver_path)

    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer config is {config_file_path}", fg=typer.colors.GREEN)

    #todo: move init_data job to config.py or data_builder.py
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
    """test"""
    #def __init__(self,data_path:Path,ip_addresses: List[str], proxy_auth: str, \
    #header: Dict[str, any], webdriver_path:str) -> None:
    if config.CONFIG_FILE_PATH.exists():
        #data_path = shopee_crawler.get_data_path(config.CONFIG_FILE_PATH)
        (data_path, ip_addresses,proxy_auth,webdriver_path,my_header) = \
            shopee_crawler.get_configs_data(config.CONFIG_FILE_PATH)

    #debug
        '''
        print(type(data_path))
        print(type(ip_addresses))
        print(type(proxy_auth))
        print(type(webdriver_path))
        print(type(my_header))
        print(my_header['user-agent'])
        '''

    else:
        typer.secho(
            'Config file not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if data_path.exists() and isinstance(ip_addresses, List) and proxy_auth \
        and webdriver_path and isinstance(my_header,Dict):
        return shopee_data_explorer.Explorer(data_path, ip_addresses,proxy_auth,\
            my_header,webdriver_path)
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
#
def read_search(
    required_args :List[str] = typer.Argument(...),
    searcher_type: int = typer.Option(1, "--searcher_type", "-t", min=1, max=2),
    retry: int = typer.Option(1, "--retry", "-r", min=1, max=5),
) -> None:
    """for test/debug, read search data"""

    print(f'inputs are {required_args}, {searcher_type}, {retry}')
    if searcher_type == 1:
        if len(required_args) != 3:
            typer.secho(
            f'{required_args} are invalid for type1 searcher', fg=typer.colors.RED
        )
            raise typer.Exit(1)
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
                raise typer.Exit(1)
            else:
                typer.secho(
                    f"""explorer: "{response['keyword']}" was searched """
                    f"""with options: page_num {response['page_num']} and page_length {response['page_length']} """
                    f"""finally it obtains the number of search result: {response['obtained_index_num']} """,
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
                    f"""finally it obtains the number of search result: {response['obtained_index_num']} """,
                    fg=typer.colors.GREEN,
                )


@app.command()
#input arg -> keyword: str, num of product: int, page_length: int (optional),
#DEFAULT_PAGE_LENGTH = 10
def scrap(
    required_args :List[str] = typer.Argument(...),
    source: int = typer.Option(0, "--scrap_source", "-ss", min=0, max=2),
    mode: int = typer.Option(0, "--scrap_mode_for_shopee", "-sm", min=0, max=2),
    searcher_type: int = typer.Option(1, "--searcher_type", "-st", min=1, max=2),
    retry: int = typer.Option(1, "--retry", "-r", min=1, max=5),
) -> None:
    """scrap source data"""
    # debug
    print(f'inputs are args - {required_args}, mode - {mode}, seacher-typr - \
        {searcher_type}, retry - {retry}')

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
            '''
            if not required_args[2]:
                page_length = shopee_crawler.DEFAULT_PAGE_LENGTH
                typer.secho(f'page_length is not given, the app will use default\
                     length:{shopee_crawler.DEFAULT_PAGE_LENGTH}', fg=typer.colors.YELLOW)
            else:
                page_length = int(required_args[2])
            '''

            explorer = get_explorer()
            response, error = explorer.scrap(keyword,num_of_product,mode,page_length)
            if error:
                typer.secho(
                    f'failed with "{ERRORS[error]}"', fg=typer.colors.RED
                )
                raise typer.Exit(1)
            else:
                typer.secho(
                    f"""explorer: "{response['keyword']}" was searched and collected sucesssfully"""
                    f"""with options: page_num {response['page_num']} and page_length \
                         {response['page_length']} """,
                    fg=typer.colors.GREEN,
                )
    else:
        print("sorry, it's not supportive yet")
        raise typer.Exit(1)






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
    """ show app version"""
    return
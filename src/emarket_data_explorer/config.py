#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------


"""This module provides the E-market Data Explorer config functionality."""
# emarket_data_explorer/config.py

import configparser
from pathlib import Path
import typer

from emarket_data_explorer import \
    (DIR_ERROR, FILE_ERROR, DATA_FOLDER_WRITE_ERROR, SUCCESS, __app_name__)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
#CONFIG_FILE_PATH = Path(typer.get_app_dir(__app_name__)).joinpath("/" + "config.ini")
CONFIG_FILE_PATH = Path(typer.get_app_dir(__app_name__)) / "config.ini"
#CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

#def init_app(data_path: str) -> int:
def init_app(**kwargs) -> int:
    """initialize the application

    Args:
        ``**kwargs`` (``**dict``): a dictionary contains the constants for the config file,\n
        such as, data_path, ip address, proxy auth...which are used to write into the config file.

    Returns:
        status code (int): SUCCESS, DIR_ERROR, DATA_FOLDER_WRITE_ERROR, see __init__.py

    """
    config_code, config_file_path = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    data_code = _create_shopee_data(kwargs)
    if data_code != SUCCESS:
        return data_code

    return SUCCESS,config_file_path

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS, CONFIG_FILE_PATH

#config.init_app(data_path=data_path,
# ip_addresses=ip_addresses, proxy_auth=proxy_auth,my_header=my_header, \
# webdriver_path=webdriver_path)

def _create_shopee_data(kwargs: dict) -> int:
    config_parser = configparser.ConfigParser(interpolation=None)
    config_parser["General"] = {"shopee_data": kwargs['data_path'],
                                "ip_addresses": kwargs['ip_addresses'],
                                "proxy_auth": kwargs['proxy_auth'],
                                #"my_header": str(kwargs['my_header']),
                                "webdriver_path": kwargs['webdriver_path'],
                                "data_source": kwargs['data_source'],
                                "db_path": kwargs['db_path'],}

    config_parser.add_section('Network-Header')
    for key in kwargs['my_header'].keys():
        config_parser.set('Network-Header',key,kwargs['my_header'][key])

    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
            #print("The config created at " + str(CONFIG_FILE_PATH))
    except OSError:
        return DATA_FOLDER_WRITE_ERROR
    return SUCCESS

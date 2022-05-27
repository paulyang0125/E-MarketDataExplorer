#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------


"""This module provides the Shopee Data Explorer config functionality."""
# shopee_data_explorer/config.py

import configparser
from pathlib import Path

import typer

from shopee_data_explorer import \
    (DIR_ERROR, FILE_ERROR, DATA_FOLDER_WRITE_ERROR, SUCCESS, __app_name__)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_app(data_path: str) -> int:
    """Initialize the application."""
    config_code, config_file_path = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    data_code = _create_shopee_data(data_path)
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

def _create_shopee_data(data_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"shopee_data": data_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
            #print("The config created at " + str(CONFIG_FILE_PATH))
    except OSError:
        return DATA_FOLDER_WRITE_ERROR
    return SUCCESS

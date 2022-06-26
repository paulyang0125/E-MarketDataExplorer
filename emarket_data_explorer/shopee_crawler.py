#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Crawler functionality.

Todo:\n
1. very ugly codes too many if-else and for-loop, need to refactor\n
2. move the following jobs to config.py or data_builder.py\n
3. should dynamically represent data_source, not 'shopee'.\n


"""
# shopee_data_explorer/shopee_crawler.py
import ast
import configparser
from pathlib import Path

import logging

#from threading import TIMEOUT_MAX

from emarket_data_explorer import (DATA_FOLDER_WRITE_ERROR,SUCCESS)



############# LOGGING #############



#todo: move the following jobs to config.py or data_builder.py
#todo: should use dynamic to represent data_source, not 'shopee'


def get_data_path(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser(interpolation=None)
    config_parser.read(config_file)
    return Path(config_parser["General"]["shopee_data"])

def get_configs_data(config_file: Path) -> Path:
    """Return the current path to the shopee_data."""
    config_parser = configparser.ConfigParser(interpolation=None)
    config_parser.read(config_file)
    #myheader = dict(config_parser['Network-Header'].items())

    return Path(config_parser["General"]["shopee_data"]),\
        ast.literal_eval(config_parser["General"]["ip_addresses"]),\
            config_parser["General"]["proxy_auth"],\
                 config_parser["General"]["webdriver_path"],\
                     config_parser["General"]["data_source"],\
                         config_parser["General"]["db_path"],\
                            dict(config_parser['Network-Header'].items())


def init_data(data_path: Path) -> int:
    """Create the shopee_data folder."""
    try:
        data_path.mkdir(parents=True, exist_ok=True)  # create the folder for shopee data
        return SUCCESS
    except OSError:
        return DATA_FOLDER_WRITE_ERROR

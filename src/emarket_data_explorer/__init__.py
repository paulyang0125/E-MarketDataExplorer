#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""Top-level package for E-market Data Explorer"""
# emarket_data_explorer/__init__.py

__app_name__ = "emarket_data_explorer"
__version__ = "1.1.0"

#errors enumeration
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    NETWORK_TIMEOUT_ERROR,
    NETWORK_CONNECTION_ERROR,
    DATA_FOLDER_WRITE_ERROR,
    READ_INDEX_ERROR,
    READ_PRODUCT_ERROR,
    READ_COMMENT_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    CSV_WRITE_ERROR,
    FIGURE_ERROR,
    EDA_ERROR,
    EMPTY_SCRAP_ERROR,

) = range(16)

#mode enumeration
(
    NA_MODE,
    ALL,
    PRODUCT_ITEMS,
    PRODUCT_COMMENTS,
    PRODUCT_INDEXES,
) = range(5)

#source enumeration
(
    NA_SOURCE,
    SHOPEE,
    PTT,
    AMAZON
) = range(4)

#mode definition

MODES = {
    ALL: "product_goods:product_comments:product_indexes",
    PRODUCT_ITEMS: "product_goods",
    PRODUCT_COMMENTS: "product_comments",
    PRODUCT_INDEXES:"product_indexes",
}

#data_source definition
DATA_SOURCES ={
    SHOPEE: "shopee",
    PTT: "ptt",
    AMAZON: "amazon"
}

#error definition
ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    NETWORK_TIMEOUT_ERROR: "download duration exceeds the preset timeout",
    NETWORK_CONNECTION_ERROR: "Connection refused. IP may be banded or network doesn't work",
    DATA_FOLDER_WRITE_ERROR: "data folder write error",
    READ_INDEX_ERROR: "read the index error",
    READ_PRODUCT_ERROR: "read the product detail error",
    READ_COMMENT_ERROR: "read the comment error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    JSON_ERROR: "json error",
    CSV_WRITE_ERROR: "csv write error",
    FIGURE_ERROR: "made figure but failed",
    EDA_ERROR: "during EDA, something goes wrong",
    EMPTY_SCRAP_ERROR: "nothing returned from scrap"
}

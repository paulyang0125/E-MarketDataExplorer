#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""Top-level package for Shopee Data Explorer"""
# shopee_data_explorer/__init__.py

__app_name__ = "shopee_data_explorer"
__version__ = "1.1.0"

#errors defintion
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

) = range(14)

#mode
(
    NA_MODE,
    ALL,
    PRODUCT_ITEMS,
    PRODUCT_COMMENTS,
) = range(4)

(
    NA_SOURCE,
    SHOPEE,
    PTT,
    AMAZON
) = range(4)

MODES = {
    ALL: "product_goods:product_comments",
    PRODUCT_ITEMS: "product_goods",
    PRODUCT_COMMENTS: "product_comments"
}

DATA_SOURCES ={
    SHOPEE: "shopee",
    PTT: "ptt",
    AMAZON: "amazon"
}

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
    FIGURE_ERROR: "made figure but failed"
}
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

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    NETWORK_TIMEOUT_ERROR,
    NETWORK_CONNECTION_ERROR,
    DATA_FOLDER_WRITE_ERROR,
    READ_INDEX_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    NETWORK_TIMEOUT_ERROR: "download duration exceeds the preset timeout",
    NETWORK_CONNECTION_ERROR: "Connection refused. IP may be banded or network doesn't work",
    DATA_FOLDER_WRITE_ERROR: "data folder write error",
    READ_INDEX_ERROR: "read the index error",
}
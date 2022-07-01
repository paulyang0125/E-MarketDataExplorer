#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Definition.

Todo:\n


"""
# shopee_data_explorer/datatype.py

from typing import Any, Dict, List, NamedTuple
import pandas as pd



class CrawlerResponse(NamedTuple):
    """data model to Crawler response"""
    result: List[Dict[str, Any]]
    error: int

class CrawlerResponseForDict(NamedTuple):
    """another data model for dict to Crawler response"""
    result: Dict[str, Any]
    error: int

class AsyncCrawlerResponse(NamedTuple):
    """data model to Crawler response"""
    results: Dict[str,Any]
    errors: List[int]


###dataclass
class ScrapingInfo(NamedTuple):
    """ data model to CLI"""
    scraping_info: Dict[str, Any]
    error: int

class ScrapingInfoForList(NamedTuple):
    """ data model for index"""
    scraping_info: List[Dict[str, Any]]
    error: int

class ScrapingInfoForDF(NamedTuple):
    """ data model for dataframe"""
    scraping_info: pd.DataFrame
    error: int

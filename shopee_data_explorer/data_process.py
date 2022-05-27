#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data process functionality."""
# shopee_data_explorer/data_process.py

import json
from typing import Any, Dict, List, NamedTuple, Tuple
from shopee_data_explorer import (DATA_FOLDER_WRITE_ERROR, SUCCESS)
import pandas as pd


class CrawlerDataProcesser:
    """data process"""

    def __init__(self) -> None:
        pass

    def process_product_data(self,product) -> Tuple[list,list,list]:
        """test"""

    def _clean_product_data(self):
        """test"""

    def process_comment_data(self,comment)-> pd.DataFrame:
        """test"""

    def aggregate_data(self, the_whole: pd.DataFrame, units: list) -> pd.DataFrame:
        """test"""


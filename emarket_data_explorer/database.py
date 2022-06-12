#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the database functionality.


Todo:\n
1. use data_source to dynamically update, not hardcoded "shopee"\n
2. implement write_index and read_index and List cli command.


"""
# shopee_data_explorer/database.py
import os
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import pandas as pd

from emarket_data_explorer import(DATA_SOURCES,\
    DB_READ_ERROR, DB_WRITE_ERROR, CSV_WRITE_ERROR, JSON_ERROR, SUCCESS)

# todo: use data_source to dynamically update, not "shopee"
DEFAULT_DB_FILE_PATH = Path.home().joinpath( "Shopee_Data" + '/' +
    "." + Path.home().stem + "_explorer_db.json"
)

Path.home().joinpath(
    "Shopee_Data"
)

class DBResponseForIndex(NamedTuple):
    """this class defines the format of database response for index in JSON"""
    response: List[Dict[str, Any]]
    error: int

class DBResponseForCSV(NamedTuple):
    """this class defines the format of database response for data in CSV"""
    response: pd.DataFrame
    error: int

class DatabaseHandler:
    """this class provides the functions of read and write into CSV and JSON for scrapped data
    """
    def __init__(self, data_path: Path, db_path: Path) -> None:
        self.owd = os.getcwd()
        self._data_path = data_path
        self._db_path = db_path

    def read_index(self) -> DBResponseForIndex:
        """read the search index data from JSON"""
        try:
            with self._db_path.open("r") as db_instance:
                try:
                    return DBResponseForIndex(json.load(db_instance), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponseForIndex([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponseForIndex([], DB_READ_ERROR)

    def write_csv(self,product_container:pd.DataFrame , my_keyword:str, data_source: int, \
        crawler_mode: str) -> DBResponseForCSV:
        """write the scrapped data stored in dataframe into CSV"""
        try:
            os.chdir(self._data_path)
            #crawler_mode = MODES[mode]
            #print("DATA_SOURCES: ", DATA_SOURCES)
            source = DATA_SOURCES[data_source]
            file_name = f'{source}_{my_keyword}_{crawler_mode}.csv'
            product_container.to_csv(file_name,encoding = 'utf-8-sig')
            print(f"the container has wrote into {file_name} in {self._data_path}")
            os.chdir(self.owd)
            return DBResponseForCSV(product_container.head(5), SUCCESS)
        except OSError:  # Catch file IO problems
            os.chdir(self.owd)
            return DBResponseForCSV(pd.DataFrame.empty, CSV_WRITE_ERROR)

    def write_index(self,product_items:pd.DataFrame) -> DBResponseForIndex:
        """write the search index data into JSON"""
        res_list = []
        res = {}
        try:
            with self._db_path.open("w") as db_instance:
                res['itemid'] = product_items['itemid'].tolist()
                res['shopid'] = product_items['shopid'].tolist()
                res['name'] = product_items['name'].tolist()
                res_list.append(res)
                json.dump(res_list, db_instance, indent=4)
                return DBResponseForIndex(res_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponseForIndex(res_list, DB_WRITE_ERROR)

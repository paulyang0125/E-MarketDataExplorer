#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 25/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------

"""This module provides the database functionality.


Todo:\n
1. use data_source to dynamically update, not hardcoded "shopee"\n
2. implement write_index and read_index and List cli command in v1.5.\n
3. remove unused datatype and also move it to the datatype file v1.4. \n
4. abstract a DatabaseHandler class and rename to ShopeeDatabaseHandler in v1.4. \n


"""
# shopee_data_explorer/database.py

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import pandas as pd

from emarket_data_explorer import(DATA_SOURCES, CSV_WRITE_ERROR, SUCCESS)


mylogger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
# create console handler with a higher log level
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
mylogger.addHandler(ch)
mylogger.addHandler(fh)




# todo: use data_source to dynamically update, not "shopee"
DEFAULT_DB_FILE_PATH = Path.home().joinpath( "Shopee_Data" + '/' +
    "." + Path.home().stem + "_explorer_db.json"
)

Path.home().joinpath(
    "Shopee_Data"
)

#todo: remove unused datatype and also move it to the datatype file
class DBResponseForIndex(NamedTuple):
    """this class defines the format of database response for index in JSON"""
    response: List[Dict[str, Any]]
    error: int

class DBResponseForCSV(NamedTuple):
    """this class defines the format of database response for data in CSV"""
    response: pd.DataFrame
    error: int


### remove ###

### remove ###


class ShopeeAsyncDatabaseHandler:
    """this class provides the functions of read and write into CSV and JSON for scrapped data
    """

    def __init__(self, data_path: Path, db_path: Path) -> None:
        self.owd = os.getcwd()
        self._data_path = data_path
        self._db_path = db_path

    def write_csv(self, product_container:pd.DataFrame,my_keyword:str, \
        data_source: int,crawler_mode: str) -> int:
        """write the scrapped data stored in dataframe into CSV"""
        try:
            os.chdir(self._data_path)
            source = DATA_SOURCES[data_source]
            file_name = f'{source}_{my_keyword}_{crawler_mode}.csv'
            #product_container = product_container.replace(r'\r+|\n+|\t+','', regex=True)
            #product_container.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"],\
            # value=["",""], regex=True, inplace=True)
            product_container.to_csv(file_name,encoding = 'utf-8-sig')
            mylogger.info("the container has wrote into %s in %s",\
                file_name, self._data_path )
            os.chdir(self.owd)
            return SUCCESS
        except OSError:  # Catch file IO problems
            os.chdir(self.owd)
            return CSV_WRITE_ERROR

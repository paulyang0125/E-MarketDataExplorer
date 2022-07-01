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
# shopee_data_explorer/crawler.py
from abc import ABC, abstractmethod

class CrawlerHandler(ABC):
    """ test """

    def __init__(self, ip_addresses,proxy_auth):

        self.ip_addresses = ip_addresses
        self.proxy_auth = proxy_auth

    @abstractmethod
    def _fetch(self,session, url, parsing_func):
        """ test """
        #pass

    @abstractmethod
    def _rotate_ip(self):
        """
        This abstract method should return a list
        :rtype: list
        """
        #pass

    @abstractmethod
    async def _download_all_sites(self,sites,parse_func):
        """ test """
        #pass

class Explorer(ABC):
    """test"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------


"""Shopee Data Explorer entry point script."""
# shopee_data_explorer/__main__.py

from shopee_data_explorer import cli, __app_name__

def main():
    """ entry of cli """
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()


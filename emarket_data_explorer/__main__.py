#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/06/2022
# version ='1.3'
# ---------------------------------------------------------------------------


"""E-market Data Explorer entry point script."""

# emarket_data_explorer/__main__.py

from emarket_data_explorer import cli, __app_name__

def main():
    """ the entry to the command interface

    Args:
        None

    Returns:
        None

    """
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()

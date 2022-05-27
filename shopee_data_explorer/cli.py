#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Paul Yang and Kana Kunikata
# Created Date: 24/05/2022
# version ='1.1'
# ---------------------------------------------------------------------------

"""This module provides the Shopee Data Explorer CLI."""
# shopee_data_explorer/cli.py
from pathlib import Path
from typing import Optional

import typer

from shopee_data_explorer import (
    ERRORS, __app_name__, __version__, config, shopee_crawler, shopee_data_explorer
)

app = typer.Typer()

@app.command()
def init(
    data_path: str = typer.Option(
        str(shopee_crawler.DEFAULT_DATA_PATH),
        "--data-path",
        "-data",
        prompt="shopee explorer data location?",
    ),
) -> None:
    """Initialize the shopee explorer data folder."""
    app_init_error,config_file_path = config.init_app(data_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer config is {config_file_path}", fg=typer.colors.GREEN)

    #todo: move init_data job to config.py or data_builder.py
    data_init_error = shopee_crawler.init_data(Path(data_path))

    if data_init_error:
        typer.secho(
            f'Creating shopee explorer data failed with "{ERRORS[data_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The shopee explorer data is {data_path}", fg=typer.colors.GREEN)

def get_explorer() -> shopee_data_explorer.Explorer:
    """test"""
    if config.CONFIG_FILE_PATH.exists():
        data_path = shopee_crawler.get_data_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if data_path.exists():
        return shopee_data_explorer.Explorer()
    else:
        typer.secho(
            'Data folder not found. Please, run "shopee_data_explorer init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """ show app version"""
    return
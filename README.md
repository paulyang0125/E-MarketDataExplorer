# E-MarketDataExplorer

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/paulyang0125/E-MarketDataExplorer)
[![Documentation Status](https://readthedocs.org/projects/e-marketdataexplorer/badge/?version=latest)](https://e-marketdataexplorer.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://app.travis-ci.com/paulyang0125/E-MarketDataExplorer.svg?branch=main)](https://app.travis-ci.com/paulyang0125/E-MarketDataExplorer)
[![codecov](https://codecov.io/gh/paulyang0125/E-MarketDataExplorer/branch/main/graph/badge.svg?token=8J6QDFONV3)](https://codecov.io/gh/paulyang0125/E-MarketDataExplorer)
[![Maintainability](https://api.codeclimate.com/v1/badges/b873efdf1a77d343aeb3/maintainability)](https://codeclimate.com/github/paulyang0125/E-MarketDataExplorer/maintainability)
![pylint Score](https://mperlet.github.io/pybadge/badges/8.53.svg)
[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/github/license/paulyang0125/E-MarketDataExplorer.svg)](https://github.com/paulyang0125/E-MarketDataExplorer/blob/main/LICENSE)


## Overview

E-Market Data Explorer is a Python crawler and exploratory data analysis(EDA) tool for marketing specialties who would like to conduct the STP methods for working out their marketing strategy for product development and sale.


## Preview

#### E-MarketDataExplorer SCRAP

![scrap-async](https://user-images.githubusercontent.com/4502089/176334966-56983073-f6dc-41c2-864b-323cd7766bf3.png)


#### E-MarketDataExplorer EDA

![app test](https://user-images.githubusercontent.com/4502089/173171695-fab53c6f-d429-466b-ab28-12c9fd57d2f9.png)


## E-MarketDataExplorer HELP

```
$ python -m emarket_data_explorer scrap-async --help

    Usage: emarket_data_explorer [OPTIONS] COMMAND [ARGS]...

    E-Market Data Explorer is a Python-based crawler and exploratory data
    analysis(EDA) tool for marketing specialties who would like to conduct the
    STP methods for working out their marketing strategy for sale and promotion.

    Updated for E-Market Data Explorer 1.5, July 2022

    Author:

    Currently written and maintained by Paul Yang <paulyang0125@gmail> and Kana
    Kunikata <vinaknkt@gmail.com>.

    Options:
    -v, --version                   Show the application's version and exit.
    --install-completion [bash|zsh|fish|powershell|pwsh]
                                    Install completion for the specified shell.
    --show-completion [bash|zsh|fish|powershell|pwsh]
                                    Show completion for the specified shell, to
                                    copy it or customize the installation.
    --help                          Show this message and exit.

    Commands:
    eda          Create EDA process and charts from csv files
    init         Initialize the shopee explorer data folder.
    scrap-async  Scrap commercial data from the data source specified by user

```


## Quick-start

Please refer to the [E-Market Data Explorer online documentation](https://e-marketdataexplorer.readthedocs.io/en/latest/index.html) for Get-Started, EDA explanation, Testing and Troubleshooting


## For Developer

API docs is under actively development but we target v1.3 to release it.


## Python Dependencies

Please refer to requirements.txt and install all the required packages by
```
$ pip install -r requirements.txt
```


## License

It is distributed under the Apache License. See LICENSE.txt for more information.


## Contact

[Paul Yang](https://github.com/paulyang0125) ; [Kana Kunikata](https://github.com/vinavinak)



E-MarketDataExplorer
====================

|GitHub tag (latest by date)| |Documentation Status| |Build Status|
|codecov| |Maintainability| |pylint Score| |image1| |image2|

Overview
--------

E-Market Data Explorer is a Python crawler and exploratory data
analysis(EDA) tool for marketing specialties who would like to conduct
the STP methods for working out their marketing strategy for product
development and sale.

Preview
-------

E-MarketDataExplorer SCRAP
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://user-images.githubusercontent.com/4502089/176334966-56983073-f6dc-41c2-864b-323cd7766bf3.png
   :alt: scrap-async

   scrap-async

E-MarketDataExplorer EDA
~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://user-images.githubusercontent.com/4502089/173171695-fab53c6f-d429-466b-ab28-12c9fd57d2f9.png
   :alt: app test

   app test

E-MarketDataExplorer HELP
-------------------------

::

   $ python -m emarket_data_explorer --help

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

Quick-start
-----------

Please refer to the `E-Market Data Explorer online
documentation <https://e-marketdataexplorer.readthedocs.io/en/latest/index.html>`__
for Get-Started, EDA explanation, Testing and Troubleshooting

.. figure:: https://user-images.githubusercontent.com/4502089/176811818-ffb5b503-cb72-444d-ae2d-0f75734c8d71.png
   :alt: doc_preview_github

   doc_preview_github

License
-------

It is distributed under the Apache License. See LICENSE.txt for more
information.

Contact
-------

`Paul Yang <https://github.com/paulyang0125>`__ ; `Kana
Kunikata <https://github.com/vinavinak>`__

Roadmap
-------

We’ve developed `our roadmap of this
utility <https://github.com/paulyang0125/E-MarketDataExplorer/wiki/E-MarketDataExplorer-Roadmap-Planning>`__.
Check it out if you’re interested in joining us.

.. |GitHub tag (latest by date)| image:: https://img.shields.io/github/v/tag/paulyang0125/E-MarketDataExplorer
.. |Documentation Status| image:: https://readthedocs.org/projects/e-marketdataexplorer/badge/?version=latest
   :target: https://e-marketdataexplorer.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://app.travis-ci.com/paulyang0125/E-MarketDataExplorer.svg?branch=main
   :target: https://app.travis-ci.com/paulyang0125/E-MarketDataExplorer
.. |codecov| image:: https://codecov.io/gh/paulyang0125/E-MarketDataExplorer/branch/main/graph/badge.svg?token=8J6QDFONV3
   :target: https://codecov.io/gh/paulyang0125/E-MarketDataExplorer
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/b873efdf1a77d343aeb3/maintainability
   :target: https://codeclimate.com/github/paulyang0125/E-MarketDataExplorer/maintainability
.. |pylint Score| image:: https://mperlet.github.io/pybadge/badges/8.53.svg
.. |image1| image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
.. |image2| image:: https://img.shields.io/github/license/paulyang0125/E-MarketDataExplorer.svg
   :target: https://github.com/paulyang0125/E-MarketDataExplorer/blob/main/LICENSE

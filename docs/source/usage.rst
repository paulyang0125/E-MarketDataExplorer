Usage
=====

.. _installation:

Installation
------------

To use e-market data explorer, first install it using pip:

.. code-block:: console

   (.venv) $ pip install e-market-data-explorer

Project Init
----------------

the first step is to initialize e-market data explorer,
you can run init command in your terminal

.. code-block:: console

   (.venv) $ e-market-data-explorer init

To retrieve a list of your input arguments,
e-market data explorer uses the ``shopee_data_explorer.cli.init()`` function:

.. autofunction:: shopee_data_explorer.cli.init

The ``data_path`` parameter should be where e-market explorer will put data on so it's
a legitimate ``"OS_path"`` in ``str`` type. Otherwise, :py:func:`shopee_data_explorer.cli.init`
will raise an exit.


.. image:: https://travis-ci.org/MacHu-GWU/pymongo_mate-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/pymongo_mate-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/pymongo_mate-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/pymongo_mate-project

.. image:: https://img.shields.io/pypi/v/pymongo_mate.svg
    :target: https://pypi.python.org/pypi/pymongo_mate

.. image:: https://img.shields.io/pypi/l/pymongo_mate.svg
    :target: https://pypi.python.org/pypi/pymongo_mate

.. image:: https://img.shields.io/pypi/pyversions/pymongo_mate.svg
    :target: https://pypi.python.org/pypi/pymongo_mate

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/pymongo_mate-project


Welcome to pymongo_mate Documentation
=====================================
A library extend pymongo module, makes CRUD easier.


Quick Links
-----------

- .. image:: https://img.shields.io/badge/Link-Document-red.svg
      :target: http://www.wbh-doc.com.s3.amazonaws.com/pymongo_mate/index.html

- .. image:: https://img.shields.io/badge/Link-API_Reference_and_Source_Code-red.svg
      :target: API reference and source code <http://www.wbh-doc.com.s3.amazonaws.com/pymongo_mate/py-modindex.html

- .. image:: https://img.shields.io/badge/Link-Install-red.svg
      :target: `install`_

- .. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/pymongo_mate-project

- .. image:: https://img.shields.io/badge/Link-Submit_Issue_and_Feature_Request-blue.svg
      :target: https://github.com/MacHu-GWU/pymongo_mate-project/issues

- .. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.python.org/pypi/pymongo_mate#downloads


Features
--------
- query builder: you don't have to remember mongodb operator syntax, just select builder from ``from pymongo_mate import query_builder as qb``, for example: ``qb.Text.startswith("/usr/bin")``
- select helper: writing complexe aggregation pipeline is pain, pymongo_mate provide functional interface to help you, just follow your human instinct.
- insert helper: a smart insert function helps you for bulk-insert with best performance, and plus, allows to insert ``pandas.DataFrame``.
- update helper.
- mongomock support: allows you to dump your mongomock database to a file. With this data persistence layer, you can use mongomock as a rich-featured pure-python faked mongodb.


.. _install:

Install
-------

``pymongo_mate`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install pymongo_mate

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade pymongo_mate
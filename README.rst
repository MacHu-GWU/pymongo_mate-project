.. image:: https://travis-ci.org/MacHu-GWU/pymongo_mate-project.svg?branch=master

.. image:: https://img.shields.io/pypi/v/pymongo_mate.svg

.. image:: https://img.shields.io/pypi/l/pymongo_mate.svg

.. image:: https://img.shields.io/pypi/pyversions/pymongo_mate.svg


Welcome to pymongo_mate Documentation
=====================================
A library extend pymongo module, makes CRUD easier.


**Quick Links**
---------------
- `GitHub Homepage <https://github.com/MacHu-GWU/pymongo_mate-project>`_
- `Online Documentation <http://www.wbh-doc.com.s3.amazonaws.com/pymongo_mate/index.html>`_
- `PyPI download <https://pypi.python.org/pypi/pymongo_mate>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/pymongo_mate-project/issues>`_
- `API reference and source code <http://www.wbh-doc.com.s3.amazonaws.com/pymongo_mate/py-modindex.html>`_


**Example**
-----------
.. code-block:: python

    from pymongo_mate import query_builder

    # find points near 32.0, -73.0 within 25 miles
    filters = {"loc": query_builder.Geo2DSphere.near(32.0, -73.0, 25, unit_miles=True)}
    for doc in collection.find(filters):
        ...

    # text query builder
    filters = {"path": query_builder.Text.startswith(r"c:\\", ignore_case=True)}
    filters = {"path": query_builder.Text.endswith(r".py"), ignore_case=True}
    filters = {"text": query_builder.Text.fulltext("python mongodb", ignore_case=True)}

    # array query builder
    filters = {"items": query_builder.Array.include_any([1, 2, 3])}
    filters = {"items": query_builder.Array.exclude_all([1, 2, 3])}


.. _install:

Install
-------

``pymongo_mate`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install pymongo_mate

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade pymongo_mate
Query Builder
==============================================================================
Example:

.. code-block:: python

    from pymongo_mate import query_builder as qb

    # find points near 32.0, -73.0 within 25 miles
    filters = {"loc": qb.Geo2DSphere.near(32.0, -73.0, 25, unit_miles=True)}
    for doc in collection.find(filters):
        ...

    # text query builder
    filters = {"path": qb.Text.startswith(r"c:\\", ignore_case=True)}
    filters = {"path": qb.Text.endswith(r".py"), ignore_case=True}
    filters = {"text": qb.Text.fulltext("python mongodb", ignore_case=True)}

    # array query builder
    filters = {"items": query_builder.Array.include_any([1, 2, 3])}
    filters = {"items": query_builder.Array.exclude_all([1, 2, 3])}

For more example, go to :mod:`~pymongo_mate.query_builder`
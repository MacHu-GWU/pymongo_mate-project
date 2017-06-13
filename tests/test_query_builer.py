#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import approx

import pymongo
from pymongo_mate.tests import col
from pymongo_mate import query_builder as qb

data = [
    {
        "_id": 1,
        "score": 10,
        "value": 3.14,
        "array": [3, 4, 5],
        "path": r"C:\Users\admin",
        "description": "$text performs a text search on the content of the fields indexed with a text index.",
        "loc": {"type": "Point", "coordinates": [-77.142901, 39.074373]},
    },
]
try:
    col.insert(data)
except:
    pass

col.create_index([("loc", pymongo.GEOSPHERE)])
col.create_index([("description", pymongo.TEXT)])


def _test(field, filters):
    assert len(list(col.find({field: filters}))) == 1


def test_operator():
    _test("value", qb.Comparison.euqal_to(3.14))
    _test("value", qb.Comparison.not_equal_to(1.414))
    _test("value", qb.Comparison.greater_than(3))
    _test("value", qb.Comparison.greater_than_equal(3.14))
    _test("value", qb.Comparison.less_than(4))
    _test("value", qb.Comparison.less_than_equal(3.14))


def test_text():
    _test("path", qb.Text.startswith("C:\\"))
    _test("path", qb.Text.endswith("admin"))
    _test("path", qb.Text.contains(r":\user"))
    assert len(list(col.find(qb.Text.fulltext("text index")))) == 1


def test_array():
    _test("score", qb.Array.item_in([10, 11]))
    _test("score", qb.Array.item_not_in([8, 9]))

    _test("array", qb.Array.include_all([3, 5]))
    _test("array", qb.Array.include_any([1, 5, 9]))
    _test("array", qb.Array.exclude_all([1, 2]))
    _test("array", qb.Array.exclude_any([1, 2, 3]))


def test_geo2dsphere():
    _test("loc",
          qb.Geo2DSphere.near(39.08, -77.14, max_dist=100000, unit_miles=False))


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])

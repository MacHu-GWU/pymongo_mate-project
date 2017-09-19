#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
from pytest import approx
import pymongo
from pymongo_mate.tests import col_real
from pymongo_mate.query_builder import *

col = col_real

data = [
    {
        "_id": 1,
        "score": 10,
        "value": 3.14,
        "array": [3, 4, 5],
        "path": r"C:\Users\admin",
        "description": "$text performs a text search on the content of the fields indexed with a text index.",
        "datetime": datetime.utcnow(),
        "loc": {"type": "Point", "coordinates": [-77.142901, 39.074373]},
        "data": [
            {"k": "a", "v": 3},
            {"k": "b", "v": 2},
            {"k": "c", "v": 1},
        ],
    },
]
try:
    col.insert(data)
except:
    pass

try:
    col.drop_indexes()
except:
    pass
col.create_index([("loc", pymongo.GEOSPHERE)])
col.create_index([("description", pymongo.TEXT)])


def _test(field, filters):
    assert len(list(col.find({field: filters}))) == 1


def test_operator():
    _test("value", Comparison.equal_to(3.14))
    _test("value", Comparison.not_equal_to(1.414))
    _test("value", Comparison.greater_than(3))
    _test("value", Comparison.greater_than_equal(3.14))
    _test("value", Comparison.less_than(4))
    _test("value", Comparison.less_than_equal(3.14))


def test_text():
    _test("path", Text.startswith("C:\\"))
    _test("path", Text.endswith("admin"))
    _test("path", Text.contains(r":\user"))
    assert len(list(col.find(Text.fulltext("text index")))) == 1


def test_array():
    _test("data", Array.element_match({"k": "b", "v": 2}))

    _test("score", Array.item_in([10, 11]))
    _test("score", Array.item_not_in([8, 9]))

    _test("array", Array.include_all([3, 5]))
    _test("array", Array.include_any([1, 5, 9]))
    _test("array", Array.exclude_all([1, 2]))
    _test("array", Array.exclude_any([1, 2, 3]))

    _test("array", Array.size(3))


def test_geo2dsphere():
    _test("loc",
          Geo2DSphere.near(39.08, -77.14, max_dist=100000, unit_miles=False))


def test_exists():
    _test("score", exists(True))
    _test("score", is_exists)


def test_mod():
    _test("score", mod(3, 1))


def test_type():
    _test("score", type_is(TypeCode.Integer32))
    _test("score", type_is(TypeCode.Number))
    _test("value", type_is(TypeCode.Double))
    _test("value", type_is(TypeCode.Number))
    #     _test("array", type_is(TypeCode.Array)) # 不知道为什么不成功
    _test("description", type_is(TypeCode.String))
    _test("datetime", type_is(TypeCode.Date))


class TestLogic(object):
    def test_and(self):
        filters = Logic.and_(
            {"value": Comparison.greater_than(3)},
            {"value": Comparison.less_than(4)},
        )
        assert col.find(filters).count() == 1

        filters = {
            "data": Array.element_match(
                Logic.and_(
                    {"v": Comparison.greater_than(1.5)},
                    {"v": Comparison.less_than(2.5)},
                )
            )
        }
        assert col.find(filters).count() == 1

    def test_or(self):
        filters = Logic.or_(
            {"value": Comparison.greater_than(3)},
            {"value": Comparison.less_than(2)},
        )
        assert col.find(filters).count() == 1

    def test_nor(self):
        filters = Logic.nor(
            {"value": Comparison.greater_than(4)},
            {"value": Comparison.less_than(3)},
        )
        assert col.find(filters).count() == 1

    def test_not(self):
        filters = {"value": Logic.not_(Comparison.equal_to(100))}
        assert col.find(filters).count() == 1


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

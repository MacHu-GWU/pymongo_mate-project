#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import warnings
import pytest
from pytest import approx
from pymongo_mate.crud.select import *
from pymongo_mate.tests import col_real, col_mock

if col_real is None:
    warnings.warn(
        "local db are not available, so some aggregation operation are not been tested")


def insert_4_data(col):
    col.remove({})
    data = [
        {"_id": 0, "v": 0},
        {"_id": 1, "v": 1},
        {"_id": 2, "v": 2},
        {"_id": 3, "v": 3},
    ]
    col.insert(data)


def insert_1000_a_b_c_data(col):
    col.remove({})

    data = list()
    _id = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                _id += 1
                data.append({"_id": _id, "a": a, "b": b, "c": c})
    col.insert(data)


def test_select_all():
    col = col_real
    insert_4_data(col)
    data = select_all(col)

    assert len(data) == 4
    assert [doc["_id"] for doc in data] == [0, 1, 2, 3]


def test_selelct_field():
    col = col_real
    insert_4_data(col)

    header, data = select_field(col, "_id")
    assert header == "_id"
    assert data == [0, 1, 2, 3]

    headers, data = select_field(
        col, ["_id", "v"], filters={"_id": {"$gte": 2}})
    assert headers == ["_id", "v"]
    assert data == [[2, 2], [3, 3]]


col = col_real
if col is not None:
    def test_select_distinct():
        insert_1000_a_b_c_data(col)

        assert select_distinct_field(col, "a") == list(range(10))
        assert len((select_distinct_field(col, ["a", "b"]))) == 100
        assert len((select_distinct_field(col, ["a", "b", "c"]))) == 1000

        assert select_distinct_field(
            col, "a", filters={"a": {"$gte": 5}}) == list(range(5, 10))
        assert len(
            select_distinct_field(col, ["a", "b"], filters={"a": {"$gte": 5}})
        ) == 50
        assert len(
            select_distinct_field(
                col, ["a", "b", "c"], filters={"a": {"$gte": 5}}
            )
        ) == 500

    def test_random_sample():
        insert_1000_a_b_c_data(col)

        assert len(random_sample(col, 5)) == 5

        result = random_sample(col, 5, filters={"_id": {"$gte": 500}})
        assert len(result) == 5
        for doc in result:
            assert doc["_id"] >= 500


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

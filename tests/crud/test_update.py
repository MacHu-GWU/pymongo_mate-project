#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import warnings
import pytest
from pytest import approx
from pymongo_mate.crud.update import *
from pymongo_mate.tests import col_real, col_mock

if col_real is None:
    warnings.warn(
        "local db are not available, so some aggregation operation are not been tested")

col = col_mock


def test_upsert_many():
    col.remove({})
    data = [
        {"_id": 0},
        {"_id": 1, "v": 0},
    ]
    col.insert(data)

    data = [
        {"_id": 0, "v": 0},
        {"_id": 1, "v": 1},
        {"_id": 2, "v": 2},
    ]
    upsert_many(col, data)
    assert list(col.find()) == [
        {'_id': 0, 'v': 0}, {'_id': 1, 'v': 1}, {'_id': 2, 'v': 2}]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

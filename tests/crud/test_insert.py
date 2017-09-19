#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import warnings
from datetime import datetime

import pytest
from pymongo_mate.crud.insert import *
from pymongo_mate.tests import col_real, col_mock

if col_real is None:
    warnings.warn(
        "local db are not available, so some aggregation operation are not been tested")

col = col_real
if col is not None:
    def test_smart_insert():
        init_n = 5
        total_n = 400

        def insert_test_data(col):
            data = [{"_id": random.randint(1, total_n)} for i in range(init_n)]
            for doc in data:
                try:
                    col.insert(doc)
                except:
                    pass
            assert col.find().count() <= init_n

        data = [{"_id": i} for i in range(1, 1 + total_n)]
        # Smart Insert
        col.remove({})
        insert_test_data(col)

        st = time.clock()
        smart_insert(col, data)
        elapse1 = time.clock() - st

        # after smart insert, we got total_n doc
        assert col.find().count() == total_n

        # Regular Insert
        col.remove({})
        insert_test_data(col)

        st = time.clock()
        for doc in data:
            try:
                col.insert(doc)
            except:
                pass
        elapse2 = time.clock() - st

        # after regular insert, we got total_n doc
        assert col.find().count() == total_n

        assert elapse1 <= elapse2


try:
    import numpy as np
    import pandas as pd

    def test_insert_data_frame():
        col = col_mock
        col.remove({})

        data = [
            ("id001", 1, 3.14, "hello".encode("utf-8"),
             datetime.now(), True, None),
        ]
        columns = "_id, int, float, binary, datetime, bool, null".split(", ")
        df = pd.DataFrame(data, columns=columns)
        insert_data_frame(col, df, int_col=None, binary_col="binary")
        res = list(col.find())

        assert data[0][0] == res[0]["_id"]
        assert data[0][1] == res[0]["int"]
        assert data[0][2] == res[0]["float"]
        assert data[0][3] == res[0]["binary"]

        assert data[0][4].year == res[0]["datetime"].year
        assert data[0][4].month == res[0]["datetime"].month
        assert data[0][4].day == res[0]["datetime"].day

        assert data[0][5] == res[0]["bool"]
        assert data[0][6] == res[0]["null"]
except ImportError:
    warnings.warn("insert_data_frame() are not tested!")
    pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pymongo
try:
    from ..utils import grouper_list
except:
    from pymongo_mate.utils import grouper_list

try:
    try:
        from .pkg.pandas_mate import transform
    except:
        from pymongo_mate.pkg.pandas_mate import transform
except:
    pass


def smart_insert(col, data, minimal_size=5):
    """An optimized Insert strategy.

    **中文文档**

    在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
    远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

    1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
    2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
    3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
      直到成功为止。

    该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
    但时间上是各种情况下平均最优的。
    """
    if isinstance(data, list):
        # 首先进行尝试bulk insert
        try:
            col.insert(data)
        # 失败了
        except pymongo.errors.DuplicateKeyError:
            # 分析数据量
            n = len(data)
            # 如果数据条数多于一定数量
            if n >= minimal_size ** 2:
                # 则进行分包
                n_chunk = math.floor(math.sqrt(n))
                for chunk in grouper_list(data, n_chunk):
                    smart_insert(col, chunk, minimal_size)
            # 否则则一条条地逐条插入
            else:
                for doc in data:
                    try:
                        col.insert(doc)
                    except pymongo.errors.DuplicateKeyError:
                        pass
    else:
        try:
            col.insert(data)
        except pymongo.errors.DuplicateKeyError:
            pass


def insert_data_frame(col, df, int_col=None, binary_col=None, minimal_size=5):
    """Insert ``pandas.DataFrame``.

    :param col: :class:`pymongo.collection.Collection` instance.
    :param df: :class:`pandas.DataFrame` instance.
    :param int_col: list of integer-type column.
    :param binary_col: list of binary-type column.
    """
    data = transform.to_dict_list_generic_type(df,
                                               int_col=int_col,
                                               binary_col=binary_col)
    smart_insert(col, data, minimal_size)


if __name__ == "__main__":
    import time
    import random
    from pymongo_mate.tests import col

    def test_smart_insert():
        def insert_test_data():
            col.remove({})

            data = [{"_id": random.randint(1, 10000)} for i in range(20)]
            for doc in data:
                try:
                    col.insert(doc)
                except:
                    pass
            assert 15 <= col.find().count() <= 20

        data = [{"_id": i} for i in range(1, 1 + 10000)]
        # Smart Insert
        insert_test_data()

        st = time.clock()
        smart_insert(col, data)
        elapse1 = time.clock() - st

        # after smart insert, we got 10000 doc
        assert col.find().count() == 10000

        # Regular Insert
        insert_test_data()

        st = time.clock()
        for doc in data:
            try:
                col.insert(doc)
            except:
                pass
        elapse2 = time.clock() - st

        # after regular insert, we got 10000 doc
        assert col.find().count() == 10000

        assert elapse1 <= elapse2

#     test_smart_insert()

    def test_insert_data_frame():
        import numpy as np
        import pandas as pd
        from datetime import datetime

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

    try:
        test_insert_data_frame()
    except ImportError:
        pass
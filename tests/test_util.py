#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pymongo_mate import utils


def test_grouper_list():
    l = list(range(10))
    res = list(utils.grouper_list(l, 3))
    assert res == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test():
    from pymongo_mate.crud.insert import *
    from pymongo_mate.crud.select import *
    from pymongo_mate.crud.update import *
    from pymongo_mate.query_builder import *


if __name__ == "__main__":
    import pytest
    pytest.main(["--tb=native", "-s"])
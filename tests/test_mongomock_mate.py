#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises

import pymongo
import mongomock
from pymongo_mate import mongomock_mate


def teardown_module(module):
    import os
    try:
        os.remove("db.json")
    except:
        pass


def test_dump_load():
    client = mongomock.MongoClient()
    db = client.db
    user_col = db.user

    user_col.insert([
        {"_id": 1, "name": "Alice"},
        {"_id": 2, "name": "Bob"},
        {"_id": 3, "name": "Cathy"},
    ])
    user_col.create_index([("name", pymongo.ASCENDING)], unique=True)

    db_data = mongomock_mate._dump(db)
    mongomock_mate.dump_db(
        db, "db.json", pretty=True, overwrite=True, verbose=False)

    # _load
    client = mongomock.MongoClient()
    db = client.db

    assert len(db._collections) == 1  # only has ``system.index`` collection
    mongomock_mate._load(db_data, db)

    assert len(db._collections) == 2
    user_col = db.user

    assert user_col.find().count() == 3
    with pytest.raises(pymongo.errors.DuplicateKeyError):
        user_col.insert_one({"_id": 4, "name": "Alice"})

    # load_db
    client = mongomock.MongoClient()
    db = client.db

    assert len(db._collections) == 1  # only has ``system.index`` collection
    mongomock_mate.load_db("db.json", db, verbose=False)

    assert len(db._collections) == 2
    user_col = db.user

    assert user_col.find().count() == 3
    with raises(pymongo.errors.DuplicateKeyError):
        user_col.insert_one({"_id": 4, "name": "Alice"})

    # _load error dbnane
    client = mongomock.MongoClient()
    db = client.test
    with raises(ValueError):
        mongomock_mate._load(db_data, db)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])

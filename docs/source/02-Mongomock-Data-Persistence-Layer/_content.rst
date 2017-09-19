Mongomock Data Persistence Layer
==============================================================================
Mongomock is an excellent library, you can use a mocked mongodb, behave like mongodb, but are not actually one. If you could have a data persistence layer, then it becomes a "real" mongodb, you can instant apply your code to real mongodb afterwards.

Dump:

.. code-block:: python

    import mongomock
    from pymongo_mate import mongodb_mate as mm

    client = mongomock.MongoClient()
    db = client.db
    user_col = db.user

    user_col.insert([
        {"_id": 1, "name": "Alice"},
        {"_id": 2, "name": "Bob"},
        {"_id": 3, "name": "Cathy"},
    ])
    user_col.create_index([("name", pymongo.ASCENDING)], unique=True)

    # dump db, compressed
    mongomock_mate.dump_db(
        db, "db.gz", pretty=True, overwrite=True, verbose=False)

Load:

.. code-block:: python

    client = mongomock.MongoClient()
    db = client.db

    mongomock_mate.load_db("db.gz", db)

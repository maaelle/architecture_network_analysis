import json
import os

import pymongo

from constants import LOGIN_MONGO_PATH


def read_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}


"""
GETTERS
"""


def get_login():
    login = read_json(LOGIN_MONGO_PATH)
    return login["username"], login["password"], login["db"]


def get_mongo_client():
    username, pwd, db = get_login()
    return pymongo.MongoClient(f"mongodb+srv://{username}:{pwd}@{db}/?retryWrites=true")


"""
PUSHERS
"""


def push_data_to_mongo_collections(collection, data):
    return get_mongo_client()[collection].insert_many(data)

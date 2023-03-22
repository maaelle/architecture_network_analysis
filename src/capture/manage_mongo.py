import json
import os

from pymongo import MongoClient

from constants import LOGIN_MONGO_PATH


def read_json(filename: str):
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
    return MongoClient(f"mongodb+srv://{username}:{pwd}@{db}/?retryWrites=true")


"""
INSERT
"""


def insert_kind_data(kind, data):
    return get_mongo_client()[kind].urls.insert_one(data)

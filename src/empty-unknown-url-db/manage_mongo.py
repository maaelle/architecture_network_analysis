import json
import os

from pymongo import MongoClient
from pymongo.results import DeleteResult

from constants import LOGIN_MONGO_PATH, MALICIOUS, UNKNOWN


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


def get_all_kind_urls(kind):
    return list(map(lambda obj: obj["url"], get_mongo_client()[kind].urls.find()))


def get_all_malicious_urls():
    return get_all_kind_urls(MALICIOUS)


def get_all_unknown_urls():
    return get_all_kind_urls(UNKNOWN)


"""
DELETES
"""


def delete_all_kind_urls(kind: str):
    return get_mongo_client()[kind].urls.delete_many({})


def delete_all_unknown_urls() -> DeleteResult:
    return delete_all_kind_urls(UNKNOWN)

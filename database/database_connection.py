from common.config_utils import get_db_credentials, get_db_name
from pymongo import MongoClient
import os
import ssl


def database_connection():
    try:
        url = get_db_credentials()
        client = MongoClient(url)
        db = client[get_db_name()]
        return db
    except Exception as e:
        print(e)
        return -1

from common.config_utils import get_db_credentials
from pymongo import MongoClient


class DbConnection:
    """
    Classe that handles interaction with mongo DB (connection, storage, retrieval)
    """

    def __init__(self):
        full_uri = get_db_credentials()
        try:
            self.connection = MongoClient(full_uri)
            print("MonogoDB connexion succeded to " + full_uri)
        except Exception as err:
            print("MonogoDB connexion failed. " + str(err))

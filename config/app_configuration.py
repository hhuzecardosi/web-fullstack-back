import json
import os

class Config:
    """Class for defining structure of configuration."""

    def __init__(self, file_name, configuration):

        self.file_name = file_name
        self.configuration = configuration
        self.app_port = None
        self.app_host = None
        self.logger = None
        self.init_config()

    def init_config(self):
        if not os.path.isfile(self.file_name):
            raise None

        with open(self.file_name) as data_file:
            item = json.load(data_file)

        # configuration application
        data_app = item.get("application", {})
        data_app = data_app.get(self.configuration, {})
        self.app_port = data_app.get("port")
        self.app_host = data_app.get("host")
        self.logger = data_app.get("Logger", {})
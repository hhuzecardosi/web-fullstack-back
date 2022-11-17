import os
from flask import Flask
from flask_cors import CORS
from common import os_utils
from config.app_configuration import Config
from routes import api
env_var = 'CONFIG_FILE'
os.environ[env_var] = os.path.join(os_utils.get_root_folder(), 'config.json')

# rv will contain the aboslute path of the config.json file
rv = os.environ.get(env_var)
if not rv:
    raise RuntimeError('The environment variable %r is not set '
                       'and as such configuration could not be '
                       'loaded.' %
                       env_var)


def create_app():
    manager_app = Flask(__name__)
    api.init_app(manager_app)
    CORS(manager_app)
    manager_app.debug = True
    return manager_app

# Deployement """
# config with environment
# config = Config(rv, "DevelopmentConfig")
# DBmodule Flask
# DBmodule = create_app()

# Local Test


app = create_app()

if __name__ == '__main__':

    # config with environment
    config = Config(rv, "DevelopmentConfig")
    # DBmodule Flask
    # run DBmodule
    app.run(debug=True, host=config.app_host, port=config.app_port)
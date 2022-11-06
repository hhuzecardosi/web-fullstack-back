import os
import codecs
import json
import common.os_utils as os_utils


#
#   Config Utils
#
#
def get_config_json(config_name):
    try:
        json_file = os.path.join(os_utils.get_root_folder(), 'config', config_name + '.json')
        with codecs.open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

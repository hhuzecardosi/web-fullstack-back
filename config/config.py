from common.os_utils import get_root_folder
import os

FILES_DIR = os.path.join(get_root_folder(), 'files')

if not os.path.exists(FILES_DIR):
    os.mkdir(FILES_DIR)

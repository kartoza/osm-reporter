import os
import shutil
from dateutil.parser import parse
from reporter import config
#from reporter.utilities import LOGGER
# This class must be refactored and tested

def mkdir_tmp():
    if os.path.exists(config.TMP_PATH):
        shutil.rmtree(config.TMP_PATH)
    os.makedirs(config.TMP_PATH)

def format_timestamp(timestamp):
    return parse(str(timestamp)).strftime("%Y-%m")

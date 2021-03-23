import json
import logging
from configvalidator import ConfigValidator

logger = logging.getLogger(__name__)

class Setup(object):

    init_status = False
    CONFIG_PATH = "./config.json"
    CHANNELS = "channels"
    RANGE = "range"
    BASE_FEE = "base_fee"
    TRANS_FEE = "trans_fee"
    TOP_LEVEL_KEYS = [CHANNELS, RANGE, BASE_FEE, TRANS_FEE]

    def validate_json(self, data):
        for i, key in enumerate(self.TOP_LEVEL_KEYS):
            if key not in data:
                raise Exception("Key "+self.TOP_LEVEL_KEYS[i]+" not found")
            curr_key = self.TOP_LEVEL_KEYS[i]            
            curr_data = data[curr_key]
            validate_data = getattr(self.configvalidator, 'validate_'+curr_key)
            validate_data(curr_data)

    def read_config(self):
        logger.debug("Opening config.json at "+self.config_file)
        with open(self.config_file, "r") as read_file:
            data = json.load(read_file)
            logger.debug("Config file opened successfully, Validating")
            self.validate_json(data)
            logger.debug("Config data validated")
            return data

    def __init__(self, config_file=None):
        self.configvalidator = ConfigValidator()
        self.config_file = config_file if config_file else self.CONFIG_PATH
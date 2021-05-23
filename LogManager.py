import os
import json
import logging.config


class LogManager:

    def __init__(self, cur_prog_name):
        default_path='logging.json'
        default_level=logging.INFO
        env_key='LOG_CFG'
        path = default_path
        value = os.getenv(env_key, None)
        self.cur_prog_name = cur_prog_name

        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)


    def get_logger(self):
        logger = logging.getLogger()
        extra = {'app_name': self.cur_prog_name}
        logger = logging.LoggerAdapter(logger, extra)

        return logger


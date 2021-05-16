# import os


class MailManager:

    def __init__(self, logger):
        self.logger = logger
        self.log_ref = ''

    # def get_logger(self):
    #     logger = logging.getLogger()
    #     extra = {'app_name': self.cur_prog_name}
    #     logger = logging.LoggerAdapter(logger, extra)
    #
    #     return logger


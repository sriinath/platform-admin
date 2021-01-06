import logging
import asyncio
import os

class FileLogger:
    def __init__(self, name='server'):
        self.logger = logging.getLogger(name=name)
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler('logs/{}.log'.format(name))
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s \nAdditional Data for the log: [%(data)s]')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)


    def get_level(self, level):
        if level == 'error':
            return logging.ERROR
        elif level == 'info':
            return logging.INFO
        elif level == 'warning':
            return logging.WARNING
        elif level == 'critical':
            return logging.INFO
        elif level == 'debug':
            return logging.DEBUG
        return None


    def log_message(self, level, message, log_info=None):
        log_level = self.get_level(level.lower() if level else '')
        if log_level:
            self.logger.log(log_level, message, extra=dict(data=log_info if log_info else None))
        else:
            self.logger.log(logging.ERROR, 'Provided level is a valid log level: {}'.format(level))


server_logger = FileLogger()
global_service_logger = FileLogger(name='global_service')

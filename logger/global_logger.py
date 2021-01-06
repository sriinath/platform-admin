import json
import requests

from constants import ENV, QUEUE_ENDPOINT
from logger.logger import global_service_logger

class LOGGER_QUEUE:
    def __init__(self, logger_endpoint=QUEUE_ENDPOINT):
        self.endpoint = logger_endpoint


    def log_messages(self, level, message, info=None):
        data = info
        resp = None
        if not data:
            data = dict()

        if self.endpoint:
            data.update(
                level=level,
                env=ENV,
                message=message
            )

            if 'source' not in data:
                data.update(source='api')
            resp = requests.post(
                self.endpoint, json=data
            )

            if resp.ok:
                return
            
        global_service_logger.log_message(
            level,
            message,
            log_info=dict(
                data,
                global_logger_status_code=resp.status_code if resp is not None else None
            )
        )

global_logger = LOGGER_QUEUE()

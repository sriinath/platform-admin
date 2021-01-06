import os
# LOG STATUS CODES

LOG_ERROR = 'ERROR'
LOG_INFO = 'INFO'
LOG_WARNING = 'WARNING'

# ERROR MESSAGES

INVALID_REQUEST_BODY = 'Payload passed for creation is not valid.'
INTERNAL_SERVER_ERROR = 'Something Went Wrong in server. Please retry again after some time.'
NO_DATA_FOUND = 'We are not able to find any data for the provided input.'

ENV = os.environ.get('ENV', 'dev')
QUEUE_ENDPOINT = os.environ.get('QUEUE_ENDPOINT')

import json
import traceback
from json.decoder import JSONDecodeError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_503_SERVICE_UNAVAILABLE, HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError
from django.db.models import ObjectDoesNotExist
from rest_framework.views import Response

from logger.global_logger import global_logger
from constants import INVALID_REQUEST_BODY, NO_DATA_FOUND, LOG_ERROR

class ExceptionHandler:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            return self.func(self, request, *args, **kwargs)
        except ObjectDoesNotExist as exc:
            message = NO_DATA_FOUND
            log_info = dict(
                payload=request.data,
                message=message,
                exception_msg=str(exc)
            )
            return self.error_response(
                message,
                HTTP_404_NOT_FOUND,
                log_info=log_info
            )
        except ValidationError as exc:
            message = INVALID_REQUEST_BODY
            log_info = dict(
                payload=request.data,
                message=message,
                exception_msg=str(exc),
                traceback_msg=traceback.format_exc()
            )
            return self.error_response(
                message,
                HTTP_400_BAD_REQUEST,
                log_info=log_info
            )
        except JSONDecodeError as exc:
            message = 'JSON provided in request body is not valid.'
            log_info = dict(
                payload=request.data,
                message=message,
                exception_msg=str(exc),
                traceback_msg=traceback.format_exc()
            )
            return self.error_response(
                message,
                HTTP_400_BAD_REQUEST,
                log_info=log_info
            )
        except AssertionError as exc:
            message = 'Please make sure the request is valid.'
            log_info = dict(
                payload=request.data,
                message=message,
                exception_msg=str(exc),
                traceback_msg=traceback.format_exc()
            )
            return self.error_response(
                message,
                HTTP_422_UNPROCESSABLE_ENTITY,
                log_info=log_info
            )
        except Exception as exc:
            message = 'Something went wrong while processing the request.'
            log_info = dict(
                payload=request.data,
                message=message,
                exception_msg=str(exc),
                traceback_msg=traceback.format_exc()
            )
            return self.error_response(
                message,
                HTTP_500_INTERNAL_SERVER_ERROR,
                log_info=log_info
            )

    def error_response(self, message, code, **kwargs):
        log_info = dict(
            status_code=code
        )
        if 'log_info' in kwargs:
            log_info = kwargs.pop('log_info')

        global_logger.log_messages(
            LOG_ERROR,
            message,
            log_info
        )
        return Response(dict(
            status='Failure',
            message=message,
            **kwargs
        ), status=code)

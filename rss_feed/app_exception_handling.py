import logging

from rest_framework.views import exception_handler

from base_app.error_codes import ApplicationErrorException
from base_app.http_helpers import bad_request


def custom_exception_handler(exe, context):
    if not isinstance(exe, ApplicationErrorException):
        response = exception_handler(exe, context)
        return response

    return bad_request(exe.http_message)

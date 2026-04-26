# core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'status':  'error',
            'message': str(exc),
            'errors':  response.data,
            'code':    response.status_code,
        }
    return response

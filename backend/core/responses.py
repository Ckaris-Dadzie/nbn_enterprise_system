# core/responses.py
from rest_framework.response import Response


def success_response(data=None, message='Success', status=200, meta=None):
    payload = {'status': 'success', 'message': message, 'data': data}
    if meta:
        payload['meta'] = meta
    return Response(payload, status=status)


def error_response(message='An error occurred', errors=None, status=400):
    payload = {'status': 'error', 'message': message}
    if errors:
        payload['errors'] = errors
    return Response(payload, status=status)

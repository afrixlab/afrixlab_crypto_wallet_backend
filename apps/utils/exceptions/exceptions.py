from django.core.exceptions import ValidationError as DjangoCoreValidationError
from rest_framework import status
from rest_framework.response import Response
from apps.utils.exceptions import (
    CustomException,
    QuerySetException
)

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status": response.status_code,
            "message": response.data,
        }

    if isinstance(exc, CustomException):
        response = Response(
            {"status": exc.status_code, "message": exc.message, "errors": exc.errors},
            status=exc.status_code,
        )
    elif isinstance(exc, QuerySetException):
        response = Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": exc.message,
                "errors": exc.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, DjangoCoreValidationError):
        response = Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": exc.message,
                "errors": exc.error_list,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return response

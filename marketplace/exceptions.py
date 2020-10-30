from django.http import JsonResponse

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_handler_404(request, exception, *args, **kwargs):
    return JsonResponse(
        data={
            'detail': 'A accessed route does not exist.',
            'code': 'not_found',
            'status_code': status.HTTP_404_NOT_FOUND
        },
        status=status.HTTP_404_NOT_FOUND
    )


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code

        if isinstance(exc, APIException):
            response.data['code'] = exc.default_code

    return response


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = (
        'The request was not answered because a conflict occurred.'
    )
    default_code = 'conflict'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)

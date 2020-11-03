from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class ClientNotFound(NotFound):
    default_detail = 'No clients found with the given ID'
    default_code = 'client_not_found'


class ClientProductFavoritesException(APIException):
    default_detail = 'An error occurred while capturing product data'
    default_code = 'product_internal_error'


class ClientProductFavoritesLockException(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = (
        'The request has been blocked because there is another request being '
        'processed by you'
    )
    default_code = 'requests_lock'


class ClientProtectedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Cannot delete the client'
    default_code = 'client_protected'

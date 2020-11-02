from rest_framework.exceptions import APIException, NotFound


class ClientNotFound(NotFound):
    default_detail = 'No clients found with the given ID'
    default_code = 'client_not_found'


class ClientProductFavoritesException(APIException):
    default_detail = 'An error occurred while capturing product data'
    default_code = 'product_internal_error'

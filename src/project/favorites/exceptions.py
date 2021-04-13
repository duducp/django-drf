from rest_framework.exceptions import APIException, NotFound


class FavoriteNotFoundApiException(NotFound):
    default_detail = 'No favorites found with the given ID'
    default_code = 'favorite_not_found'


class ClientNotFoundApiException(NotFound):
    default_detail = 'Informed client does not exist in the database'
    default_code = 'client_not_found'


class ProductNotFoundApiException(NotFound):
    default_detail = 'Informed product does not exist'
    default_code = 'product_not_found'


class ProductRequestApiException(APIException):
    default_detail = 'Failed to get product data'
    default_code = 'product_internal_error'

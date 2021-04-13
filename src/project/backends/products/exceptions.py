class ProductException(Exception):
    pass


class ProductTimeoutException(ProductException):
    pass


class ProductNotFoundException(ProductException):
    pass


class ProductValidationException(ProductException):
    pass


class ProductClientException(ProductException):
    def __init__(
        self,
        message='',
        status_code=None,
        response=None,
        payload=None
    ):
        self.status_code = status_code
        self.response = response
        self.payload = payload
        self.message = message

    def __repr__(self):
        return self.message

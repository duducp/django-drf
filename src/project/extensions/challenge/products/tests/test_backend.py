from unittest.mock import patch

import pytest

from project.backends.products.exceptions import (
    ProductClientException,
    ProductException,
    ProductNotFoundException,
    ProductTimeoutException,
    ProductValidationException
)
from project.backends.products.interfaces import Product
from project.extensions.challenge.products.backend import ProductBackend
from project.extensions.challenge.products.exceptions import (
    ChallengeProductClientException,
    ChallengeProductException,
    ChallengeProductNotFoundException,
    ChallengeProductTimeoutException
)


class TestGetProduct:
    @pytest.fixture
    def mock_get_product(self, mock_data_api_product):
        with patch(
            'project.extensions.challenge.products.backend.'
            'get_product'
        ) as mock:
            mock.return_value = mock_data_api_product
            yield mock

    def test_should_validate_the_return_when_function_is_called(
        self,
        mock_get_product,
        mock_data_api_product,
        product_id,
    ):
        backend = ProductBackend()
        response = backend.get_product(product_id)

        mock_get_product.assert_called_once_with(product_id)
        assert isinstance(response, Product)
        assert response == Product.from_dict(mock_data_api_product)

    def test_should_validate_return_when_function_throws_a_not_found_exception(
        self,
        mock_get_product,
        mock_data_api_product,
        product_id,
        mock_logger,
    ):
        mock_get_product.side_effect = ChallengeProductNotFoundException

        with pytest.raises(ProductNotFoundException):
            backend = ProductBackend()
            backend.get_product(product_id)

        mock_logger.error.assert_called_once_with(
            'Product API returned product id not found',
            error_message=''
        )
        mock_logger.bind(product_id=product_id)

    def test_should_validate_return_when_function_throws_a_client_exception(
        self,
        mock_get_product,
        mock_data_api_product,
        product_id,
        mock_logger,
    ):
        mock_get_product.side_effect = ChallengeProductClientException

        with pytest.raises(ProductClientException):
            backend = ProductBackend()
            backend.get_product(product_id)

        mock_logger.error.assert_called_once_with(
            'Product API error in request',
            status_code=None,
            response=None,
            error_message=''
        )

    def test_should_validate_return_when_function_throws_a_timeout_exception(
        self,
        mock_get_product,
        mock_data_api_product,
        product_id,
        mock_logger,
    ):
        mock_get_product.side_effect = ChallengeProductTimeoutException

        with pytest.raises(ProductTimeoutException):
            backend = ProductBackend()
            backend.get_product(product_id)

        mock_logger.error.assert_called_once_with(
            'Product API error was timeout',
            error_message=''
        )

    def test_should_validate_return_when_function_throws_a_generic_exception(
        self,
        mock_get_product,
        mock_data_api_product,
        product_id,
        mock_logger,
    ):
        mock_get_product.side_effect = ChallengeProductException

        with pytest.raises(ProductException):
            backend = ProductBackend()
            backend.get_product(product_id)

        mock_logger.critical.assert_called_once_with(
            'Client Product Challenge API generic error',
            error_message='',
            exc_info=True
        )

    def test_should_validate_return_when_function_throws_a_validation_exception(  # noqa
        self,
        mock_get_product,
        mock_data_api_product,
        mock_logger,
        product_id,
    ):
        mock_data_api_product.pop('price')
        mock_get_product.return_value = mock_data_api_product

        with pytest.raises(ProductValidationException):
            backend = ProductBackend()
            backend.get_product(product_id)

        mock_logger.error.assert_called_once_with(
            'Error in validating the data returned by the external API',
            error_message=(
                "{'price': [ErrorDetail(string='This field is required.', "
                "code='required')]}"
            )
        )

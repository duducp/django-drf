import json
from urllib.parse import urljoin

import pytest
import responses
from requests import Timeout
from simple_settings import settings

from marketplace.apps.extensions.challenge.products.exceptions import (
    ChallengeProductClientException,
    ChallengeProductException,
    ChallengeProductNotFoundException,
    ChallengeProductTimeoutException
)
from marketplace.apps.extensions.challenge.products.http_client import (
    get_product
)


class TestGetProduct:
    challenge_settings = settings.EXTENSIONS_CONFIG['challenge']

    @pytest.fixture
    def url(self, product_id):
        return urljoin(
            self.challenge_settings['host'],
            self.challenge_settings['routes']['product']
        ).format(
            product_id=product_id
        )

    @pytest.fixture
    def mock_data_not_found_api(self, product_id):
        return {
            'error_message': f'Product {product_id} not found',
            'code': 'not_found'
        }

    @responses.activate
    def test_should_validate_the_return_of_the_api_when_the_request_occurs_successfully(  # noqa
        self,
        url,
        product_id,
        mock_data_api_product,
    ):
        responses.add(
            responses.GET,
            url,
            json=mock_data_api_product,
            status=200
        )
        data = get_product(product_id)
        assert data == mock_data_api_product

    @responses.activate
    def test_should_return_exception_not_found_when_the_product_does_not_exist(
        self,
        url,
        product_id,
        mock_data_not_found_api,
    ):
        responses.add(
            responses.GET,
            url,
            json=mock_data_not_found_api,
            status=404
        )
        with pytest.raises(ChallengeProductNotFoundException):
            get_product(product_id)

    @responses.activate
    def test_should_return_client_exception_when_api_returns_an_error(
        self,
        url,
        product_id,
        mock_data_not_found_api,
    ):
        responses.add(
            responses.GET,
            url,
            json=mock_data_not_found_api,
            status=401
        )
        with pytest.raises(ChallengeProductClientException) as exc:
            get_product(product_id)

        assert exc.value.status_code == 401
        assert exc.value.response == json.dumps(mock_data_not_found_api)

    @responses.activate
    def test_should_return_exception_timeout_when_api_takes_too_long_to_respond(  # noqa
        self,
        url,
        product_id,
        mock_data_not_found_api,
    ):
        responses.add(
            responses.GET,
            url,
            body=Timeout()
        )
        with pytest.raises(ChallengeProductTimeoutException):
            get_product(product_id)

    @responses.activate
    def test_should_return_product_exception_when_a_generic_error_occurs(
        self,
        url,
        product_id,
        mock_data_not_found_api,
    ):
        responses.add(
            responses.GET,
            url,
            body=Exception()
        )
        with pytest.raises(ChallengeProductException):
            get_product(product_id)

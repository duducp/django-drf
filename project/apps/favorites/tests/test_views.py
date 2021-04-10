from unittest.mock import Mock, patch
from uuid import UUID

import pytest

from project.apps.favorites.models import Favorite
from project.apps.favorites.tests.schemas import FavoriteSchema
from project.apps.helpers.backends.products.exceptions import (
    ProductException,
    ProductNotFoundException
)


@pytest.mark.django_db
class TestFavoriteCreateView:
    contract = FavoriteSchema()

    @pytest.fixture()
    def data_post(self, client):
        return {
            'client_id': str(client.id),
            'product_id': '6a512e6c-6627-d286-5d18-583558359ab6',
        }

    @pytest.fixture()
    def mock_logger(self):
        with patch(
            'project.apps.favorites.views.logger'
        ) as mock:
            yield mock

    @pytest.fixture()
    def mock_get_product(self):
        with patch(
            'project.apps.favorites.serializers.ProductBackend'
        ) as mock:
            mock_return_value = Mock()
            mock_return_value.get_product = Mock(name='mock_get_product')
            mock.return_value = mock_return_value
            yield mock

    def test_should_validates_if_the_client_has_been_registered(
        self,
        client_authenticated,
        data_post,
        mock_logger,
        mock_get_product,
    ):
        response = client_authenticated.post(
            path='/v1/favorites/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 201
        assert self.contract.validate(data, self.contract.schema)
        mock_logger.info.assert_called_once_with(
            'Data received to create favorite',
            data=data_post
        )
        mock_get_product.return_value.get_product.assert_called_once_with(
            UUID(data_post['product_id'])
        )

        count = Favorite.objects.count()
        assert count == 1

    def test_should_valid_when_favorite_is_already_registered(
        self,
        client_authenticated,
        data_post,
        favorite,
        mock_get_product,
    ):
        response = client_authenticated.post(
            path='/v1/favorites/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 409
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'conflict'

    def test_should_valid_when_client_id_informed_not_exists_in_database(
        self,
        client_authenticated,
        favorite,
        mock_get_product,
    ):
        response = client_authenticated.post(
            path='/v1/favorites/',
            data={
                'client_id': '6a512e6c-6627-d286-5d18-583558359ab6',
                'product_id': '6a512e6c-6627-d286-5d18-583558359ab6',
            },
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_not_found'

    def test_should_valid_when_product_id_informed_not_exists(
        self,
        client_authenticated,
        data_post,
        favorite,
        mock_get_product,
    ):
        mock_return_value = Mock()
        mock_return_value.get_product = Mock(
            side_effect=ProductNotFoundException
        )
        mock_get_product.return_value = mock_return_value

        response = client_authenticated.post(
            path='/v1/favorites/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'product_not_found'

    def test_should_valid_when_request_for_valid_product_id_throw_exception(
        self,
        client_authenticated,
        data_post,
        favorite,
        mock_get_product,
    ):
        mock_return_value = Mock()
        mock_return_value.get_product = Mock(
            side_effect=ProductException
        )
        mock_get_product.return_value = mock_return_value

        response = client_authenticated.post(
            path='/v1/favorites/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 500
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'product_internal_error'

    def test_should_return_errors_related_to_serializer_when_body_is_invalid(
        self,
        client_authenticated
    ):
        response = client_authenticated.post(
            path='/v1/favorites/',
            data={},
            format='json'
        )
        data = response.json()

        assert response.status_code == 400
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'invalid'
        pytest.assume(data.get('client_id'))
        pytest.assume(data.get('product_id'))

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        data_post
    ):
        response = client_unauthenticated.post(
            path='/v1/favorites/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestFavoriteDestroyView:
    contract = FavoriteSchema()

    def test_should_should_return_status_code_204_when_favorite_is_successfully_deleted(  # noqa
        self,
        client_authenticated,
        favorite,
    ):
        response = client_authenticated.delete(
            path=f'/v1/favorites/{str(favorite.id)}/',
            format='json'
        )

        assert response.status_code == 204

    def test_should_valid_returned_when_it_does_not_find_favorite(
        self,
        client_authenticated,
    ):
        response = client_authenticated.delete(
            path='/v1/favorites/sdfsf/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'favorite_not_found'

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        favorite,
    ):
        response = client_unauthenticated.delete(
            path=f'/v1/favorites/{favorite.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)

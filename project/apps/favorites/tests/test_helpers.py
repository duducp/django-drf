from unittest.mock import Mock, patch

import pytest
from model_bakery import baker

from project.apps.favorites.helpers import get_details_products_favorites
from project.apps.favorites.models import Favorite
from project.apps.helpers.backends.products.exceptions import (
    ProductNotFoundException
)
from project.apps.helpers.backends.products.interfaces import Product


@pytest.mark.django_db
class TestGetDetailsProductsFavorites:
    @pytest.fixture()
    def product_interface(self):
        return Product(
            id='6a512e6c-6627-d286-5d18-583558359ab6',
            brand='bébé confort',
            price=1149.0,
            image='http://challenge-api.luizalabs.com/images/6.jpg',
            title='Moisés Dorel Windoo 1529'
        )

    @pytest.fixture()
    def mock_get_product(self, product_interface):
        with patch(
            'project.apps.favorites.helpers.ProductBackend'
        ) as mock:
            mock_return_value = Mock()
            mock_return_value.get_product = Mock(
                return_value=product_interface
            )
            mock.return_value = mock_return_value
            yield mock

    @pytest.fixture()
    def client_model(self):
        yield baker.make(
            'clients.Client',
            email='test@email.com'
        )

    @pytest.fixture()
    def favorite_model(self, client_model):
        yield baker.make(
            'favorites.Favorite',
            client=client_model,
            product_id='6a512e6c-6627-d286-5d18-583558359ab6',
            id='ff31f647-f872-4e70-b886-fd3071cd2788'
        )

    @pytest.fixture()
    def favorites_list(self, client_model):
        return [
            {
                'id': 'ff31f647-f872-4e70-b886-fd3071cd2788',
                'client_id': client_model.id,
                'product_id': '6a512e6c-6627-d286-5d18-583558359ab6'
            }
        ]

    def test_should_validate_the_return_when_successful(
        self,
        mock_get_product,
        client_model,
        favorites_list,
    ):
        favorites_expected = [
            {
                'id': 'ff31f647-f872-4e70-b886-fd3071cd2788',
                'client_id': client_model.id,
                'product_id': '6a512e6c-6627-d286-5d18-583558359ab6',
                'product': {
                    'id': '6a512e6c-6627-d286-5d18-583558359ab6',
                    'price': 1149.0,
                    'image': 'http://challenge-api.luizalabs.com/images/6.jpg',
                    'brand': 'bébé confort',
                    'title': 'Moisés Dorel Windoo 1529'
                }
            }
        ]
        favorites_detail = get_details_products_favorites(favorites_list)

        assert favorites_expected == favorites_detail
        mock_get_product.return_value.get_product.assert_called_once_with(
            '6a512e6c-6627-d286-5d18-583558359ab6'
        )

    def test_should_validate_that_favorite_has_been_deleted_when_product_does_not_exist(  # noqa
        self,
        mock_get_product,
        product_interface,
        favorite_model,
        favorites_list,
        client_model,
    ):
        mock_return_value = Mock()
        mock_return_value.get_product = Mock(
            side_effect=ProductNotFoundException
        )
        mock_get_product.return_value = mock_return_value

        with patch(
            'project.apps.favorites.helpers.logger'
        ) as mock_logger:
            favorites_detail = get_details_products_favorites(favorites_list)

        assert favorites_detail == []
        assert Favorite.objects.count() == 0
        mock_logger.info.assert_called_once_with(
            'Removing the favorite because the product does not exist',
            product_id='6a512e6c-6627-d286-5d18-583558359ab6',
            client_id=str(client_model.id)
        )

from unittest.mock import patch

import pytest
from django_toolkit.concurrent.locks import LockActiveError
from model_bakery import baker

from marketplace.apps.backends.products.exceptions import ProductException
from marketplace.apps.clients.models import Client
from marketplace.apps.clients.tests.schemas import ClientSchema


@pytest.mark.django_db
class TestClientCreateView:
    contract = ClientSchema()

    @pytest.fixture()
    def data_post(self):
        return {
            'name': 'Carlos',
            'last_name': 'Eduardo',
            'email': 'test@email.com',
        }

    def test_should_validates_if_client_has_been_registered(
        self,
        client_authenticated,
        data_post
    ):
        response = client_authenticated.post(
            path='/v1/clients/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 201
        assert self.contract.validate(data, self.contract.schema)

        count_clients = Client.objects.count()
        assert count_clients == 1

    def test_should_valid_when_client_is_already_registered(
        self,
        client_authenticated,
        data_post
    ):
        baker.make(
            'clients.Client',
            email='test@email.com'
        )

        response = client_authenticated.post(
            path='/v1/clients/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 409
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'conflict'

    def test_should_return_errors_related_to_serializer(
        self,
        client_authenticated
    ):
        response = client_authenticated.post(
            path='/v1/clients/',
            data={},
            format='json'
        )
        data = response.json()

        assert response.status_code == 400
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'invalid'
        pytest.assume(data.get('name'))
        pytest.assume(data.get('last_name'))
        pytest.assume(data.get('email'))

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        data_post
    ):
        response = client_unauthenticated.post(
            path='/v1/clients/',
            data=data_post,
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientListView:
    contract = ClientSchema()

    def test_should_return_a_client_who_is_registered(
        self,
        client_authenticated,
    ):
        baker.make(
            'clients.Client',
            _quantity=20
        )

        response = client_authenticated.get(
            path='/v1/clients/?limit=2',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.list_schema)

    def test_should_valid_returned_when_it_does_not_find_client(
        self,
        client_authenticated
    ):
        response = client_authenticated.get(
            path='/v1/clients/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert self.contract.validate(
            data,
            self.contract.list_without_results_schema
        )
        assert data['count'] == 0

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
    ):
        response = client_unauthenticated.get(
            path='/v1/clients/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientRetrieveView:
    contract = ClientSchema()

    def test_should_return_a_client_who_is_registered(
        self,
        client_authenticated,
        client_model
    ):
        response = client_authenticated.get(
            path=f'/v1/clients/{client_model.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.retrieve_schema)

    def test_should_valid_returned_when_it_does_not_find_client(
        self,
        client_authenticated
    ):
        response = client_authenticated.get(
            path='/v1/clients/sadasd/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_not_found'

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        client_model
    ):
        response = client_unauthenticated.get(
            path=f'/v1/clients/{client_model.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientUpdateView:
    contract = ClientSchema()

    @pytest.fixture()
    def data_update(self):
        return {
            'name': 'Carlos',
            'last_name': 'Eduardo',
            'email': 'test@email.com'
        }

    def test_should_valid_if_client_has_been_updated(
        self,
        client_authenticated,
        client_model,
        data_update
    ):
        response = client_authenticated.put(
            path=f'/v1/clients/{client_model.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()
        client_model.refresh_from_db()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.update_schema)
        assert data['name'] == 'Carlos'
        assert client_model.name == 'Carlos'

    def test_should_valid_returned_when_it_does_not_find_client(
        self,
        client_authenticated,
        data_update
    ):
        response = client_authenticated.put(
            path='/v1/clients/sdfsf/',
            data=data_update,
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_not_found'

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        client_model,
        data_update
    ):
        response = client_unauthenticated.put(
            path=f'/v1/clients/{client_model.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientPartialUpdateView:
    contract = ClientSchema()

    @pytest.fixture()
    def data_update(self):
        return {
            'name': 'Carlos'
        }

    def test_should_valid_if_client_has_been_updated(
        self,
        client_authenticated,
        client_model,
        data_update
    ):
        response = client_authenticated.patch(
            path=f'/v1/clients/{client_model.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()
        client_model.refresh_from_db()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.update_schema)
        assert data['name'] == 'Carlos'
        assert client_model.name == 'Carlos'

    def test_should_valid_returned_when_it_does_not_find_client(
        self,
        client_authenticated,
        data_update
    ):
        response = client_authenticated.patch(
            path='/v1/clients/sdfsf/',
            data=data_update,
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_not_found'

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        client_model,
        data_update
    ):
        response = client_unauthenticated.patch(
            path=f'/v1/clients/{client_model.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientDestroyView:
    contract = ClientSchema()

    def test_should_return_status_code_204_when_client_is_successfully_deleted(  # noqa
        self,
        client_authenticated,
        client_model,
    ):
        response = client_authenticated.delete(
            path=f'/v1/clients/{str(client_model.id)}/',
            format='json'
        )

        assert response.status_code == 204

    def test_should_valid_returned_when_it_does_not_find_client(
        self,
        client_authenticated,
    ):
        response = client_authenticated.delete(
            path='/v1/clients/sdfsf/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 404
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_not_found'

    def test_should_valid_returned_when_client_is_protected(
        self,
        client_authenticated,
        client_model,
    ):
        baker.make(
            'favorites.Favorite',
            client=client_model,
            product_id='eaefc867-10a6-3a5e-947d-43a984964fcf'
        )

        response = client_authenticated.delete(
            path=f'/v1/clients/{str(client_model.id)}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 400
        assert self.contract.validate(data, self.contract.error_schema)
        assert data['code'] == 'client_protected'

    def test_should_checks_whether_route_is_protected(
        self,
        client_unauthenticated,
        client_model,
    ):
        response = client_unauthenticated.delete(
            path=f'/v1/clients/{client_model.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientFavoritesDetailView:
    @pytest.fixture()
    def favorite_list(self, client_model):
        return [
            {
                'id': 'ff31f647-f872-4e70-b886-fd3071cd2788',
                'client_id': str(client_model.id),
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

    @pytest.fixture()
    def favorite_model(self, client_model):
        yield baker.make(
            'favorites.Favorite',
            client=client_model,
            product_id='1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        )

    @pytest.fixture()
    def mock_get_details_product(self, favorite_list):
        with patch(
            'marketplace.apps.clients.views.get_details_products_favorites'
        ) as mock:
            mock.return_value = favorite_list
            yield mock

    def test_should_validate_return_when_search_for_data_is_successful(
        self,
        client_authenticated,
        client_model,
        favorite_model,
        mock_get_details_product,
        favorite_list,
    ):
        response = client_authenticated.get(
            path=f'/v1/clients/{str(client_model.id)}/favorites/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert data == favorite_list
        mock_get_details_product.assert_called_once()

    def test_should_validate_return_when_an_error_occurs_for_fetching_product_data(  # noqa
        self,
        client_authenticated,
        client_model,
        favorite_model,
        mock_get_details_product,
        favorite_list,
    ):
        mock_get_details_product.side_effect = ProductException

        response = client_authenticated.get(
            path=f'/v1/clients/{str(client_model.id)}/favorites/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 500
        assert data == {
            'detail': 'An error occurred while capturing product data',
            'status_code': 500,
            'code': 'product_internal_error'
        }

    def test_should_validate_return_when_error_occurs_many_requests(
        self,
        client_authenticated,
        client_model,
        favorite_model,
        mock_get_details_product,
        favorite_list,
    ):
        with patch(
            'marketplace.apps.clients.views.CacheLock'
        ) as mock_cache_lock:
            mock_cache_lock.side_effect = LockActiveError

            response = client_authenticated.get(
                path=f'/v1/clients/{str(client_model.id)}/favorites/',
                format='json'
            )
            data = response.json()

        assert response.status_code == 429
        assert data == {
            'detail': (
                'The request has been blocked because there is another request'
                ' being processed by you'
            ),
            'status_code': 429,
            'code': 'requests_lock'
        }
        mock_cache_lock.assert_called_once_with(
            key=f'cachelock:retrieve_favorites_{str(client_model.id)}',
            cache_alias='concurrent',
            expire=30
        )
        mock_get_details_product.assert_not_called()

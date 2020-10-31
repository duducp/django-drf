import pytest
from model_bakery import baker

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

    def test_should_validates_if_the_client_has_been_registered(
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

    def test_should_valid_when_customer_is_already_registered(
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

    def test_should_should_return_errors_related_to_the_serializer(
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

    def test_should_checks_whether_the_route_is_protected(
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

    def test_should_return_a_customer_who_is_registered(
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

    def test_should_valid_the_returned_when_it_does_not_find_the_client(
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

    def test_should_checks_whether_the_route_is_protected(
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

    def test_should_return_a_customer_who_is_registered(
        self,
        client_authenticated,
        client
    ):
        response = client_authenticated.get(
            path=f'/v1/clients/{client.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.retrieve_schema)

    def test_should_valid_the_returned_when_it_does_not_find_the_client(
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

    def test_should_checks_whether_the_route_is_protected(
        self,
        client_unauthenticated,
        client
    ):
        response = client_unauthenticated.get(
            path=f'/v1/clients/{client.id}/',
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

    def test_should_valid_if_the_client_has_been_updated(
        self,
        client_authenticated,
        client,
        data_update
    ):
        response = client_authenticated.put(
            path=f'/v1/clients/{client.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()
        client.refresh_from_db()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.update_schema)
        assert data['name'] == 'Carlos'
        assert client.name == 'Carlos'

    def test_should_valid_the_returned_when_it_does_not_find_the_client(
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

    def test_should_checks_whether_the_route_is_protected(
        self,
        client_unauthenticated,
        client,
        data_update
    ):
        response = client_unauthenticated.put(
            path=f'/v1/clients/{client.id}/',
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

    def test_should_valid_if_the_client_has_been_updated(
        self,
        client_authenticated,
        client,
        data_update
    ):
        response = client_authenticated.patch(
            path=f'/v1/clients/{client.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()
        client.refresh_from_db()

        assert response.status_code == 200
        assert self.contract.validate(data, self.contract.update_schema)
        assert data['name'] == 'Carlos'
        assert client.name == 'Carlos'

    def test_should_valid_the_returned_when_it_does_not_find_the_client(
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

    def test_should_checks_whether_the_route_is_protected(
        self,
        client_unauthenticated,
        client,
        data_update
    ):
        response = client_unauthenticated.patch(
            path=f'/v1/clients/{client.id}/',
            data=data_update,
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)


@pytest.mark.django_db
class TestClientDestroyView:
    contract = ClientSchema()

    @pytest.fixture()
    def client(self):
        yield baker.make(
            'clients.Client',
            email='test@email.com'
        )

    def test_should_should_return_status_code_204_when_customer_is_successfully_deleted(  # noqa
        self,
        client_authenticated,
    ):
        client = baker.make(
            'clients.Client',
            email='test@email.com'
        )

        response = client_authenticated.delete(
            path=f'/v1/clients/{str(client.id)}/',
            format='json'
        )

        assert response.status_code == 204

    def test_should_valid_the_returned_when_it_does_not_find_the_client(
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

    def test_should_checks_whether_the_route_is_protected(
        self,
        client_unauthenticated,
        client,
    ):
        response = client_unauthenticated.delete(
            path=f'/v1/clients/{client.id}/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 401
        assert self.contract.validate(data, self.contract.error_schema)

import pytest
from model_bakery import baker

from project.clients.models import Client


@pytest.mark.django_db
class TestClientModel:

    @pytest.fixture
    def client_model(self):
        yield baker.make(
            'Client',
            name='Carlos Eduardo',
            last_name='Dorneles',
            email='test@email.com'
        )

    def test_client_creation(self, client_model):
        assert isinstance(client_model, Client)
        assert client_model.__str__() == 'Carlos Eduardo Dorneles'

    def test_should_valid_return_property_full_name_when_called(
        self,
        client_model
    ):
        assert client_model.full_name == 'Carlos Eduardo Dorneles'

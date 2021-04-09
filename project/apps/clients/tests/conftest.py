import pytest
from model_bakery import baker


@pytest.fixture()
def client_model():
    model = baker.make(
        'clients.Client',
        name='Carlos Eduardo',
        last_name='Dorneles',
        email='test@email.com'
    )
    yield model

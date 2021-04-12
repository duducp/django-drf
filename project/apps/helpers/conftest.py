import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def user_model():
    yield baker.make(
        'User',
        username='duducp'
    )


@pytest.fixture
def client_authenticated(user_model):
    client = APIClient()
    client.force_authenticate(user=user_model)
    yield client


@pytest.fixture
def client_unauthenticated(client_authenticated):
    client_unauthenticated = client_authenticated
    client_unauthenticated.force_authenticate(user=None)
    yield client_unauthenticated

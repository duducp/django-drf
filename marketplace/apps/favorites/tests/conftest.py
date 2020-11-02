import pytest
from model_bakery import baker


@pytest.fixture()
def client():
    yield baker.make(
        'clients.Client'
    )


@pytest.fixture()
def favorite(client):
    yield baker.make(
        'favorites.Favorite',
        client_id=client.id,
        product_id='6a512e6c-6627-d286-5d18-583558359ab6'
    )

from django.db import IntegrityError

import pytest
from model_bakery import baker

from marketplace.apps.favorites.models import Favorite


@pytest.mark.django_db
class TestFavoriteModel:

    @pytest.fixture
    def client_model(self):
        yield baker.make(
            'Client',
            name='Carlos Eduardo',
            last_name='Dorneles',
            email='test@email.com'
        )

    @pytest.fixture
    def favorite_model(self, client_model):
        yield baker.make(
            'Favorite',
            client=client_model,
            product_id='6a512e6c-6627-d286-5d18-583558359ab6',
        )

    def test_favorite_creation(self, favorite_model):
        assert isinstance(favorite_model, Favorite)

    def test_should_ensure_that_client_id_and_product_id_are_unique_when_trying_to_register_a_favorite(  # noqa
        self,
        favorite_model,
        client_model,
    ):
        with pytest.raises(IntegrityError):
            baker.make(
                'Favorite',
                client=client_model,
                product_id='6a512e6c-6627-d286-5d18-583558359ab6',
            )

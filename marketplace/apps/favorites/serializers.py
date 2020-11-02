from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from marketplace.apps.backends.products.exceptions import (
    ProductException,
    ProductNotFoundException
)
from marketplace.apps.backends.products.serializers import ProductSerializer
from marketplace.apps.clients.models import Client
from marketplace.apps.extensions.challenge.products.backend import (
    ProductBackend
)
from marketplace.apps.favorites.models import Favorite


class FavoriteCreateSerializer(ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(
        source='client',
        queryset=Client.objects
    )

    @staticmethod
    def validate_product_id(value):
        try:
            backend = ProductBackend()
            backend.get_product(value)
        except ProductNotFoundException:
            raise serializers.ValidationError(
                detail='Informed product does not exist in the database',
                code='does_not_exist'
            )
        except ProductException:
            raise serializers.ValidationError(
                detail='Failed to get product data',
                code='error_request'
            )

        return value

    class Meta:
        model = Favorite
        fields = ('id', 'client_id', 'product_id', 'created_at', 'updated_at')
        read_only_fields = ['id']


class FavoriteDetailSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'client_id', 'product_id', 'product']

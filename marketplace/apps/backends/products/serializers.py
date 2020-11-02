from rest_framework import serializers

from marketplace.apps.backends.products.interfaces import Product


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        write_only=True,
        allow_null=False,
        required=True
    )
    title = serializers.CharField(
        allow_null=False,
        required=True
    )
    price = serializers.FloatField(
        allow_null=False,
        required=True
    )
    brand = serializers.CharField(
        allow_null=False,
        required=True
    )
    image = serializers.CharField(
        allow_null=False,
        required=True
    )

    def from_interface(self):
        return Product.from_dict(self.initial_data)

    def is_valid(
        self,
        raise_exception=False,
        cache=None,
        remove_cache=False,
        key_cache=''
    ):
        validated = super().is_valid(raise_exception)
        if not validated and cache and remove_cache:
            cache.delete(key_cache)

        return validated

    def create(self, validated_data):
        return Product.from_dict(validated_data)

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        return instance

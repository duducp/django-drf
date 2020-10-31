from rest_framework.serializers import ModelSerializer

from marketplace.apps.clients.models import Client


class ClientListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name']


class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientCreateSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id']


class ClientUpdateSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id']


class ClientProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']


class ClientProductListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['name']


class ClientOrderListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['full_name']


class ClientOrderDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name']

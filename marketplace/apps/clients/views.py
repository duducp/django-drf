from django.db.models.deletion import ProtectedError
from django.http import Http404

import structlog
from django_toolkit.concurrent.locks import CacheLock, LockActiveError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from marketplace.apps.backends.products.exceptions import ProductException
from marketplace.apps.clients.exceptions import (
    ClientNotFound,
    ClientProductFavoritesException,
    ClientProductFavoritesLockException,
    ClientProtectedException
)
from marketplace.apps.clients.models import Client
from marketplace.apps.clients.serializers import (
    ClientCreateSerializer,
    ClientDetailSerializer,
    ClientListSerializer,
    ClientUpdateSerializer
)
from marketplace.apps.favorites.helpers import get_details_products_favorites
from marketplace.apps.favorites.models import Favorite
from marketplace.apps.favorites.serializers import FavoriteDetailSerializer
from marketplace.exceptions import Conflict

logger = structlog.get_logger(__name__)


class ClientFavoriteDetailView(GenericViewSet):
    lookup_field = 'client_id'
    queryset = Favorite.objects
    serializer_class = FavoriteDetailSerializer

    @swagger_auto_schema(
        operation_summary='List the client favorite products',
        responses={
            200: FavoriteDetailSerializer(many=True),
            404: 'Favorites not found for client',
        },
    )
    @action(methods=['GET'], detail=True, url_path='favorites')
    def retrieve_favorites(self, request, client_id=None):
        try:
            with CacheLock(
                key=f'cachelock:retrieve_favorites_{client_id}',
                cache_alias='concurrent',
                expire=30,
            ):
                logger.info(
                    'Searching for favorite products',
                    client_id=client_id
                )

                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                favorites = get_details_products_favorites(
                    favorites=serializer.data
                )

                return Response(
                    data=favorites,
                    status=status.HTTP_200_OK
                )
        except ProductException:
            raise ClientProductFavoritesException
        except LockActiveError:
            raise ClientProductFavoritesLockException


class ClientListView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientListSerializer
        elif self.request.method == 'POST':
            return ClientCreateSerializer

    @swagger_auto_schema(
        operation_summary='List all clients',
        responses={
            200: ClientListSerializer(many=True),
        },
    )
    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(
            data=serializer.data
        )

    @swagger_auto_schema(
        operation_summary='Create client',
        request_body=ClientCreateSerializer,
        responses={
            201: ClientCreateSerializer(),
            400: 'Invalid body',
            409: 'Conflict',
        },
    )
    def create(self, request):
        try:
            logger.info(
                'Data received to create client',
                data=request.data
            )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data)
            )
        except ValidationError as exc:
            email = exc.detail.get('email')
            if email and email[0].code == 'unique':
                raise Conflict(detail=str(email[0]))
            raise


class ClientDetailView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Client.objects

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer
        elif self.request.method in ('PUT', 'PATCH'):
            return ClientUpdateSerializer

    @swagger_auto_schema(
        operation_summary='List one client',
        responses={
            200: ClientDetailSerializer(),
            404: 'Client not found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            client = self.get_object()
            serializer = self.get_serializer(client)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Http404:
            raise ClientNotFound

    @swagger_auto_schema(
        operation_summary='Update all attributes do client',
        request_body=ClientUpdateSerializer,
        responses={
            200: ClientUpdateSerializer(),
            400: 'Invalid body',
            404: 'Client not found',
        },
    )
    def update(self, request, pk=None):
        try:
            logger.info(
                'Data received to update client',
                pk=pk,
                data=request.data
            )

            client = self.get_object()
            serializer = self.get_serializer(client, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Http404:
            raise ClientNotFound

    @swagger_auto_schema(
        operation_summary='Update partial attributes do client',
        request_body=ClientUpdateSerializer,
        responses={
            200: ClientUpdateSerializer(),
            400: 'Invalid body',
            404: 'Client not found',
        },
    )
    def partial_update(self, request, pk=None):
        try:
            logger.info(
                'Data received to update client',
                pk=pk,
                data=request.data
            )

            client = self.get_object()
            serializer = self.get_serializer(
                client,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Http404:
            raise ClientNotFound

    @swagger_auto_schema(
        operation_summary='Removes the client',
        responses={
            204: 'Success',
            404: 'Client not found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            logger.info(
                'Request for client deleting',
                pk=pk
            )

            client = self.get_object()
            client.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            raise ClientNotFound
        except ProtectedError:
            raise ClientProtectedException

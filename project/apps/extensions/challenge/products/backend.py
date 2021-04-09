from typing import Optional

from django.core.cache import cache

import structlog
from rest_framework.exceptions import ValidationError
from simple_settings import settings

from project.apps.backends.products.backend import ProductAbstractBackend
from project.apps.backends.products.exceptions import (
    ProductClientException,
    ProductException,
    ProductNotFoundException,
    ProductTimeoutException,
    ProductValidationException
)
from project.apps.backends.products.interfaces import Product
from project.apps.backends.products.serializers import ProductSerializer
from project.apps.extensions.challenge.products.exceptions import (
    ChallengeProductClientException,
    ChallengeProductException,
    ChallengeProductNotFoundException,
    ChallengeProductTimeoutException
)
from project.apps.extensions.challenge.products.http_client import get_product

logger = structlog.get_logger(__name__)


class ProductBackend(ProductAbstractBackend):
    @staticmethod
    def _get_serializer(data, many=False):
        return ProductSerializer(data=data, many=many)

    @staticmethod
    def _get_key_cache(product_id: str) -> str:
        return f'product-{product_id}'

    def _set_data_cache(self, product_id: str, data: dict) -> None:
        cache.set(
            key=self._get_key_cache(product_id),
            value=data,
            timeout=settings.EXTENSIONS_CONFIG['challenge']['caches']['product']  # noqa
        )

    def _get_data_cache(self, product_id: str) -> Optional[Product]:
        cache_key = self._get_key_cache(product_id)
        cache_data = cache.get(cache_key)
        if cache_data:
            serializer = self._get_serializer(data=cache_data)
            validated = serializer.is_valid(
                cache=cache,
                key_cache=cache_key,
                remove_cache=True
            )
            if validated:
                return serializer.from_interface()

        return None

    def get_product(self, product_id: str) -> Product:
        try:
            logger.bind(product_id=product_id)

            cache_data = self._get_data_cache(product_id)
            if cache_data:
                logger.info(
                    'Product data returned by cache',
                    product_data=cache_data,
                )
                return cache_data

            data = get_product(product_id)
            serializer = self._get_serializer(data)
            serializer.is_valid(raise_exception=True)

            self._set_data_cache(
                data=serializer.data,
                product_id=product_id
            )

            return serializer.from_interface()

        except ValidationError as exc:
            logger.error(
                'Error in validating the data returned by the external API',
                error_message=str(exc)
            )
            raise ProductValidationException from exc

        except ChallengeProductNotFoundException as exc:
            logger.error(
                'Product API returned product id not found',
                error_message=str(exc)
            )
            raise ProductNotFoundException from exc

        except ChallengeProductClientException as exc:
            logger.error(
                'Product API error in request',
                status_code=exc.status_code,
                response=exc.response,
                error_message=str(exc)
            )
            raise ProductClientException from exc

        except ChallengeProductTimeoutException as exc:
            logger.error(
                'Product API error was timeout',
                error_message=str(exc)
            )
            raise ProductTimeoutException from exc

        except ChallengeProductException as exc:
            logger.critical(
                'Client Product Challenge API generic error',
                error_message=str(exc),
                exc_info=True
            )
            raise ProductException from exc

from typing import Optional

from django.core.cache import cache

import structlog
from rest_framework.exceptions import ValidationError
from simple_settings import settings

from marketplace.apps.backends.products.backend import ProductAbstractBackend
from marketplace.apps.backends.products.exceptions import (
    ProductClientException,
    ProductException,
    ProductNotFoundException,
    ProductTimeoutException,
    ProductValidationException
)
from marketplace.apps.backends.products.interfaces import Product
from marketplace.apps.backends.products.serializers import ProductSerializer
from marketplace.apps.extensions.challenge.products.exceptions import (
    ChallengeProductClientException,
    ChallengeProductException,
    ChallengeProductNotFoundException,
    ChallengeProductTimeoutException
)
from marketplace.apps.extensions.challenge.products.http_client import (
    get_product
)

logger = structlog.get_logger(__name__)


class ProductBackend(ProductAbstractBackend):
    @staticmethod
    def _get_serializer(data, many=False):
        return ProductSerializer(data=data, many=many)

    def _get_data_cache(self, key: str, product_id: str) -> Optional[Product]:
        cache_data = cache.get(key)
        if cache_data:
            serializer = self._get_serializer(data=cache_data)
            validated = serializer.is_valid(
                raise_exception=False,
                cache=cache,
                key_cache=key,
                remove_cache=True
            )
            if validated:
                logger.info(
                    'Product data returned by cache',
                    product_data=cache_data,
                    product_id=product_id
                )
                return serializer.from_interface()

        return None

    def get_product(self, product_id: str) -> Product:
        try:
            cache_key = f'product-{product_id}'
            cache_data = self._get_data_cache(cache_key, product_id)
            if cache_data:
                return cache_data

            data = get_product(product_id)
            serializer = self._get_serializer(data)
            serializer.is_valid(raise_exception=True)

            cache.set(
                key=cache_key,
                value=serializer.data,
                timeout=settings.CACHES_TTL['product']
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
                product_id=product_id,
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

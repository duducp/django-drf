from typing import Dict, List

import structlog

from project.backends.products.exceptions import ProductNotFoundException
from project.extensions.challenge.products.backend import ProductBackend
from project.favorites.models import Favorite

logger = structlog.get_logger(__name__)


def get_details_products_favorites(favorites: List[Dict]) -> List:
    backend = ProductBackend()

    for index, favorite in enumerate(favorites):
        product_id = favorite['product_id']
        client_id = str(favorite['client_id'])
        favorite_id = favorite['id']

        try:
            product_interface = backend.get_product(product_id)
            favorite['product'] = product_interface.as_dict()
        except ProductNotFoundException:
            logger.info(
                'Removing the favorite because the product does not exist',
                product_id=product_id,
                client_id=client_id
            )
            Favorite.objects.get(pk=favorite_id).delete()
            favorites.pop(index)

    return favorites

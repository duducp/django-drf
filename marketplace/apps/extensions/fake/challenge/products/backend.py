from marketplace.apps.backends.products.backend import ProductAbstractBackend
from marketplace.apps.backends.products.interfaces import Product


class ProductFakeBackend(ProductAbstractBackend):

    def get_product(self, product_id: str) -> Product:
        data = {
            'price': 1699.0,
            'image': (
                'http://challenge-api.luizalabs.com/images/'
                '1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg'
            ),
            'brand': 'bébé confort',
            'id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
        }
        return Product.from_dict(data)

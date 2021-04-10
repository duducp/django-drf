import abc

from project.apps.helpers.backends.products.interfaces import Product


class ProductAbstractBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_product(self, product_id: str) -> Product:
        pass

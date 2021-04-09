import abc

from project.apps.backends.products.interfaces import Product


class ProductAbstractBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_product(self, product_id: str) -> Product:
        pass

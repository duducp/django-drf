from project.backends.products.interfaces import Product
from project.extensions.fake.challenge.products.backend import (
    ProductFakeBackend
)


class TestBackend:

    def test_should_validate_whether_get_product_will_return_a_dataclass_when_called(  # noqa
        self
    ):
        backend = ProductFakeBackend()
        response = backend.get_product(
            product_id='1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        )
        assert isinstance(response, Product)

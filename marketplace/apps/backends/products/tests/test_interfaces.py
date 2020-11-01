from marketplace.apps.backends.products.interfaces import Product


class TestProductInterface:

    def test_should_validate_the_type_returned_when_the_as_dict_function_is_called(  # noqa
        self,
    ):
        data = Product(
            id='58ec015-cfcf-258d-c6df-1721de0ab6ea',
            price=10.9,
            image='http://challenge-api.luizalabs.com/images/8359ab6.jpg',
            brand='bébé confort',
            title='Moisés Dorel Windoo 1529'
        ).as_dict()
        assert isinstance(data, dict)

    def test_should_validate_the_type_returned_when_the_from_dict_function_is_called(  # noqa
        self,
    ):
        payload = {
            'price': 1149.0,
            'image': 'http://challenge-api.luizalabs.com/images/6a512e666.jpg',
            'brand': 'bébé confort',
            'id': '6a512e6c-6627-d286-5d18-583558359ab6',
            'title': 'Moisés Dorel Windoo 1529'
        }
        data = Product.from_dict(payload)
        assert isinstance(data, Product)

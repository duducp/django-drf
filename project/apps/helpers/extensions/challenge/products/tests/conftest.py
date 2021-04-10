from unittest.mock import patch

import pytest


@pytest.fixture
def mock_logger():
    with patch(
        'project.apps.helpers.extensions.challenge.products.backend.logger'
    ) as mock:
        yield mock


@pytest.fixture
def product_id():
    return '1bf0f365-fbdd-4e21-9786-da459d78dd1f'


@pytest.fixture
def mock_data_api_product():
    return {
        'price': 1699.0,
        'image': (
            'http://challenge-api.luizalabs.com/images/'
            '1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg'
        ),
        'brand': 'bébé confort',
        'id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
        'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
    }

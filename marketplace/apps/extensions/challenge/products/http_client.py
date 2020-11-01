from http import HTTPStatus
from urllib.parse import urljoin

import requests
from requests import HTTPError, Timeout
from simple_settings import settings

from marketplace.apps.extensions.challenge.products.exceptions import (
    ChallengeProductClientException,
    ChallengeProductException,
    ChallengeProductNotFoundException,
    ChallengeProductTimeoutException
)

challenge_settings = settings.EXTENSIONS_CONFIG['challenge']


def get_product(product_id: str) -> dict:
    try:
        url = urljoin(
            challenge_settings['host'],
            challenge_settings['routes']['product']
        ).format(
            product_id=product_id
        )

        response = requests.get(
            url=url,
            timeout=challenge_settings['timeout'],
        )
        response.raise_for_status()

        data = response.json()
        return data

    except HTTPError as exc:
        status_code = exc.response.status_code

        if status_code == HTTPStatus.NOT_FOUND:
            raise ChallengeProductNotFoundException(
                'Products Challenge API returned error product not found',
            ) from exc

        raise ChallengeProductClientException(
            'Product Challenge API returned an error in the request',
            status_code=status_code,
            response=exc.response.text,
        ) from exc

    except Timeout as exc:
        raise ChallengeProductTimeoutException(
            'There was a timeout error during the requisition to '
            'Product Challenge'
        ) from exc

    except Exception as exc:
        raise ChallengeProductException(
            'An unhandled error occurred when making a request to '
            'Product Challenge'
        ) from exc

import pytest

from project import __version__


@pytest.mark.django_db
class TestPingView:
    def test_should_validate_the_return_when_a_call_occurs_on_the_route(
        self,
        client_unauthenticated
    ):
        response = client_unauthenticated.get(
            path='/ping/',
            format='json'
        )
        data = response.json()

        assert response.status_code == 200
        assert data == {
            'message': 'pong',
            'version': __version__,
            'datetime': data.get('datetime')
        }

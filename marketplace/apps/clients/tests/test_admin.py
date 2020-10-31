import pytest

from marketplace.apps.clients.admin import ClientAdmin


class TestAdmin:
    def test_should_validate_static_elements_of_admin_when_it_is_called(self):
        client_class = ClientAdmin
        list_display = client_class.list_display
        search_fields = client_class.search_fields
        list_per_page = client_class.list_per_page
        list_max_show_all = client_class.list_max_show_all

        list_display_expected = [
            'id',
            'full_name',
            'email',
            'created_at',
            'updated_at',
        ]
        search_fields_expected = [
            'email',
            'last_name',
            'name'
        ]

        pytest.assume(list_display == list_display_expected)
        pytest.assume(search_fields == search_fields_expected)
        pytest.assume(list_per_page == 30)
        pytest.assume(list_max_show_all == 30)

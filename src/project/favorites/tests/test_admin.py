import pytest

from project.favorites.admin import FavoriteAdmin


class TestAdmin:
    def test_should_validate_static_elements_of_admin_when_it_is_called(self):
        favorite_class = FavoriteAdmin
        list_display = favorite_class.list_display
        search_fields = favorite_class.search_fields
        list_per_page = favorite_class.list_per_page
        list_max_show_all = favorite_class.list_max_show_all

        list_display_expected = [
            'id',
            'product_id',
            'created_at',
            'updated_at',
        ]
        search_fields_expected = [
            'id',
            'product_id',
            'client__id',
            'client__name'
        ]

        pytest.assume(list_display == list_display_expected)
        pytest.assume(search_fields == search_fields_expected)
        pytest.assume(list_per_page == 30)
        pytest.assume(list_max_show_all == 30)

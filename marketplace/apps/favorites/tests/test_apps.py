from marketplace.apps.favorites.apps import FavoritesConfig


class TestApps:
    def test_should_be_successful_when_application_name_is_as_expected(self):
        app_name = FavoritesConfig.name

        assert app_name == 'favorites'

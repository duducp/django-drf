from marketplace.apps.clients.apps import ClientsConfig


class TestApps:
    def test_should_be_successful_when_application_name_is_as_expected(self):
        app_name = ClientsConfig.name

        assert app_name == 'clients'

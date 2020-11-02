from marketplace.apps.ping.apps import PingConfig


class TestApps:
    def test_should_be_successful_when_application_name_is_as_expected(self):
        app_name = PingConfig.name

        assert app_name == 'ping'

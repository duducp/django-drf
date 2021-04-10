from unittest.mock import patch

import pytest

from project.apps.helpers.contracts import Contract


class TestContracts:
    @pytest.fixture()
    def mock_logger(self):
        with patch(
            'project.apps.helpers.contracts.logger'
        ) as mock_logger:
            yield mock_logger

    def test_should_return_true_when_schema_is_valid(
        self,
        mock_logger,
    ):
        schema = {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'}
            },
            'additionalProperties': True,
            'required': ['detail']
        }
        data = {
            'detail': 'test'
        }
        validated = Contract().validate(data, schema)

        assert validated
        mock_logger.info.assert_called_once_with(
            'Contract valid'
        )

    def test_should_return_false_when_contract_is_invalid(
        self,
        mock_logger,
    ):
        schema = {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'}
            },
            'additionalProperties': True,
            'required': ['detail']
        }
        data = {
            'test': 'test'
        }
        validated = Contract().validate(data, schema)

        assert not validated
        mock_logger.info.assert_called_once_with(
            "Contract invalid: 'detail' is a required property"
        )

    def test_should_return_false_when_schema_is_invalid(
        self,
        mock_logger,
    ):
        schema = {
            'type': {'type': 'string'}
        }
        data = {
            'type': 'test'
        }
        validated = Contract().validate(data, schema)

        assert not validated
        mock_logger.info.assert_called_once_with(
            "Schema invalid: {'type': 'string'} is not valid under any of the "
            'given schemas'
        )

    def test_should_validate_the_return_when_the_error_schema_property_is_called(  # noqa
        self
    ):
        schema = Contract().error_schema

        assert schema == {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'},
                'status_code': {'type': 'integer'},
                'code': {'type': 'string'},
            },
            'additionalProperties': True,
            'required': ['status_code', 'code']
        }

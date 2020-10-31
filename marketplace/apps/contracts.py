from typing import Any

import structlog
from jsonschema import FormatChecker, SchemaError, ValidationError, validate

logger = structlog.get_logger(__name__)


class Contract:
    @staticmethod
    def validate(data: Any, schema: dict) -> bool:
        try:
            validate(data, schema, format_checker=FormatChecker())
            logger.info('Contract valid')
            return True
        except SchemaError as ex:
            logger.info(f'Schema invalid: {ex.message}')
            return False
        except ValidationError as ex:
            logger.info(f'Contract invalid: {ex.message}')
            return False

    @property
    def error_schema(self) -> dict:
        return {
            'type': 'object',
            'properties': {
                'detail': {'type': 'string'},
                'status_code': {'type': 'integer'},
                'code': {'type': 'string'},
            },
            'additionalProperties': True,
            'required': ['status_code', 'code']
        }

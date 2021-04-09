from project.apps.contracts import Contract


class ClientSchema(Contract):
    @property
    def schema(self) -> dict:
        properties = {
            'id': {'type': 'string', 'format': 'uuid'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'updated_at': {'type': 'string', 'format': 'date-time'},
            'name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'},
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

    @property
    def list_without_results_schema(self) -> dict:
        properties = {
            'count': {'type': 'integer'},
            'next': {'type': ['string', 'null'], 'format': 'uri'},
            'previous': {'type': ['string', 'null'], 'format': 'uri'},
            'results': {
                'type': 'array'
            }
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

    @property
    def list_schema(self) -> dict:
        results = {
            'id': {'type': 'string', 'format': 'uuid'},
            'full_name': {'type': 'string'},
        }

        properties = {
            'count': {'type': 'integer'},
            'next': {'type': ['string', 'null'], 'format': 'uri'},
            'previous': {'type': ['string', 'null'], 'format': 'uri'},
            'results': {
                'type': 'array',
                'items': [
                    {
                        'type': 'object',
                        'properties': results,
                        'additionalProperties': False,
                        'required': list(results.keys())
                    }
                ]
            }
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

    @property
    def retrieve_schema(self) -> dict:
        properties = {
            'id': {'type': 'string', 'format': 'uuid'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'updated_at': {'type': 'string', 'format': 'date-time'},
            'name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'},
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

    @property
    def update_schema(self) -> dict:
        properties = {
            'id': {'type': 'string', 'format': 'uuid'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'updated_at': {'type': 'string', 'format': 'date-time'},
            'name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'},
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

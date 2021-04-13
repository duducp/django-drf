from project.helpers.contracts import Contract


class FavoriteSchema(Contract):
    @property
    def schema(self) -> dict:
        properties = {
            'id': {'type': 'string', 'format': 'uuid'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'updated_at': {'type': 'string', 'format': 'date-time'},
            'client_id': {'type': 'string'},
            'product_id': {'type': 'string'},
        }

        return {
            'type': 'object',
            'properties': properties,
            'additionalProperties': False,
            'required': list(properties.keys())
        }

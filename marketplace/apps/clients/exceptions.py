from rest_framework.exceptions import NotFound


class ClientNotFound(NotFound):
    default_detail = 'No clients found with the given ID.'
    default_code = 'client_not_found'

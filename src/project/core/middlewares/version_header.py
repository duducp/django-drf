from django.utils.deprecation import MiddlewareMixin

from project import __version__


class VersionHeaderMiddleware(MiddlewareMixin):
    """
    Add a X-API-Version header to the response.
    """

    @staticmethod
    def process_response(request, response):
        response['X-API-Version'] = __version__
        return response

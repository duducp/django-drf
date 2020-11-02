from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from simple_settings import settings

schema_view = get_schema_view(
    openapi.Info(
        title=settings.APPLICATION['name'],
        default_version=settings.REST_FRAMEWORK['DEFAULT_VERSION'],
        description="""
        To make a request on a protected route, you must inform the header **Authorization** with the obtained token. Ex.: `Authorization: Bearer TOKEN`.

        The header **Accept** can also be informed in the request to define the type of data to be returned. Today, only `application/xml` and` application/json` are supported.
        You can also enter the query string **format** with the value of **json** or **xml**. Ex.: /?format=json

        In every request, the header **X-Correlation-ID** will always be returned, which is the unique ID of the request, very useful for logs.
        The **X-Api-Version** header is also returned, which is the application version at the time of the request.
        """,
        terms_of_service=settings.APPLICATION['terms_of_service'],
        contact=openapi.Contact(
            name=settings.APPLICATION['contact']['name'],
            email=settings.APPLICATION['contact']['email'],
        ),
    ),
    public=settings.APPLICATION['doc_public'],
    permission_classes=(
        permissions.AllowAny,
    ),
)

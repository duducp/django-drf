from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from simple_settings import settings

schema_view = get_schema_view(
    openapi.Info(
        title=settings.APPLICATION['name'],
        default_version='v1',
        description="""
        To make a request on a protected route, you must inform the header **Authorization** with the obtained token. Ex.: `Authorization: Bearer TOKEN`.

        The header **Accept** can also be informed in the request to define the type of data to be returned. Today, only `application/xml` and` application/json` are supported.

        In every request, the header **X-Correlation-ID** will always be returned, which is the unique ID of the request, very useful for logs.
        """,
        terms_of_service=settings.APPLICATION['terms_of_service'],
        contact=openapi.Contact(
            name=settings.APPLICATION['contact']['name'],
            email=settings.APPLICATION['contact']['email'],
        ),
    ),
    public=settings.APPLICATION['doc_public'],
    permission_classes=(permissions.AllowAny,),
)

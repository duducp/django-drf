from typing import List

from django.contrib import admin
from django.urls import include, path

from marketplace.exceptions import custom_handler_404
from marketplace.swagger import schema_view

handler404 = custom_handler_404

auth = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]

routers_v1: List = [
    path('docs/', schema_view.with_ui('swagger')),
    path('auth/', include(auth)),
    path('clients/', include('marketplace.apps.clients.urls')),
    path('favorites/', include('marketplace.apps.favorites.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', include('health_check.urls')),
    path('ping/', include('marketplace.apps.ping.urls')),
    path('v1/', include((routers_v1, 'v1'), namespace='v1')),
]

from typing import List

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from simple_settings import settings

from project.core.exceptions import custom_handler_404
from project.core.swagger import schema_view

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE

handler404 = custom_handler_404

auth: List = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]

routers_v1: List = [
    path('docs/', schema_view.with_ui('swagger')),
    path('auth/', include(auth)),
    path('clients/', include('project.clients.urls')),
    path('favorites/', include('project.favorites.urls')),
]

admin_i18n: List = i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    prefix_default_language=True
)

urlpatterns: List = [
    path('healthcheck/', include('health_check.urls')),
    path('ping/', include('project.ping.urls')),
    path('v1/', include((routers_v1, 'v1'), namespace='v1')),
] + admin_i18n

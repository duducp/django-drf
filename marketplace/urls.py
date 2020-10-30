from typing import List

from django.contrib import admin
from django.urls import include, path

from marketplace.exceptions import custom_handler_404

handler404 = custom_handler_404

routers_v1: List = [

]

urlpatterns = [
    path('v1/', include((routers_v1, 'v1'), namespace='v1')),
    path('admin/', admin.site.urls),
]

from django.urls import path

from ..ping import views

urlpatterns = [
    path('', views.PingView.as_view())
]

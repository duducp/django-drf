from django.urls import path

from marketplace.apps.ping import views

urlpatterns = [
    path('', views.PingView.as_view())
]

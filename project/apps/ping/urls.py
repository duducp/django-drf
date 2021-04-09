from django.urls import path

from project.apps.ping import views

urlpatterns = [
    path('', views.PingView.as_view())
]

from rest_framework import routers

from marketplace.apps.clients import views

router = routers.DefaultRouter(trailing_slash=True)
router.register('clients', views.ClientListView)
router.register('clients', views.ClientDetailView)

urlpatterns = router.urls

from rest_framework import routers

from marketplace.apps.clients import views

router = routers.DefaultRouter(trailing_slash=True)
router.register('clients', views.ClientListView)
router.register('clients', views.ClientDetailView)
router.register('clients', views.ClientFavoriteDetailView)

urlpatterns = router.urls

from rest_framework import routers

from marketplace.apps.clients import views

router = routers.DefaultRouter(trailing_slash=True)
router.register('', views.ClientListView)
router.register('', views.ClientDetailView)
router.register('', views.ClientFavoriteDetailView)

urlpatterns = router.urls

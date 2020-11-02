from rest_framework import routers

from marketplace.apps.favorites import views

router = routers.DefaultRouter(trailing_slash=True)
router.register('favorites', views.FavoriteListView)
router.register('favorites', views.FavoriteDetailView)

urlpatterns = router.urls

from rest_framework import routers

from project.favorites import views

router = routers.DefaultRouter(trailing_slash=True)
router.register('', views.FavoriteListView)
router.register('', views.FavoriteDetailView)

urlpatterns = router.urls

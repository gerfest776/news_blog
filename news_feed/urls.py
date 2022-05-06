from rest_framework.routers import DefaultRouter

from news_feed.views import NewsViewSet

router = DefaultRouter(trailing_slash=False)
router.register("news", NewsViewSet)

urlpatterns = []
urlpatterns += router.urls

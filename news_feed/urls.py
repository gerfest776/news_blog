from django.urls import path
from rest_framework.routers import DefaultRouter

from news_feed.views import NewsViewSet

router = DefaultRouter(trailing_slash=False)
router.register("news", NewsViewSet)

router._urls = [
    r for r in router.urls if not any([r.name.endswith(bad) for bad in ["detail"]])
]

urlpatterns = [
    path("news", NewsViewSet.as_view({"get": "list"})),
]
urlpatterns += router.urls

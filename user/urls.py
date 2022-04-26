from rest_framework.routers import DefaultRouter

from user.views import UserCreateViewSet

router = DefaultRouter(trailing_slash=False)
router.register("create", UserCreateViewSet)

urlpatterns = []
urlpatterns += router.urls

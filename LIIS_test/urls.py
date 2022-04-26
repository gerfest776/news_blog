from typing import Any

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


def get_swagger() -> Any:
    swagger = get_schema_view(
        openapi.Info(
            title="Upload API",
            default_version="v1",
            contact=openapi.Contact(email="email"),
        ),
        public=True,
        generator_class=APISchemeGenerator,
    )
    return swagger


schema_view = get_swagger()
urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("api/", include("news_feed.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

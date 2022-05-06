from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

import user.permissions
from news_feed.models import Article
from news_feed.pagination import Pagination
from news_feed.serializers import (
    NewsCreateSerializer,
    NewsEditSerialzier,
    NewsListSerializer,
)
from news_feed.service.querysets import author_article_list, private_news_list


class NewsViewSet(
    UpdateModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Article.objects.filter(type="open")
    serializer_class = NewsListSerializer  #
    pagination_class = Pagination

    def get_queryset(self):
        if self.action == "news_private":
            return private_news_list(self.request.user.id)
        if self.request.method in ["PATCH", "PUT"]:
            return author_article_list(self.request.user.id)
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewsCreateSerializer
        if self.request.method in ["PATCH", "PUT"]:
            return NewsEditSerialzier
        return self.serializer_class

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return [
                user.permissions.IsAuthor(),
            ]
        elif self.action == "news_private":
            return [
                permissions.IsAuthenticated(),
            ]
        return [
            permissions.AllowAny(),
        ]

    @action(methods=["get"], detail=False, url_path="subscriptions")
    def news_private(self, request):
        return self.list(request)

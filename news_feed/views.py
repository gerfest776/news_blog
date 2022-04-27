from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

import user.permissions
from news_feed.models import Article
from news_feed.pagination import Pagination
from news_feed.serializers import (
    NewsCreateSerializer,
    NewsEditSerialzier,
    NewsListSerializer,
)
from news_feed.service.querysets import (
    author_article_list,
    private_news_list,
)


class NewsViewSet(
    UpdateModelMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Article.objects.filter(type="open")
    serializer_class = NewsListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        if self.action == "news_private":
            return private_news_list(self.request.user.id)
        if self.action == "news_edit":
            return author_article_list(self.request.user.id)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "news_create":
            return NewsCreateSerializer
        elif self.action == "news_edit":
            return NewsEditSerialzier
        return self.serializer_class

    def get_permissions(self):
        if self.action == "news_create" or self.action == "news_edit":
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

    @action(methods=["post"], detail=False, url_path="create")
    def news_create(self, request):
        return self.create(request)

    @action(methods=["get"], detail=False, url_path="subscriptions")
    def news_private(self, request):
        return self.list(request)

    @action(methods=["patch", "delete"], detail=True, url_path="edit")
    def news_edit(self, request, pk):
        if request.method == "PATCH":
            return self.partial_update(request)

        # delete
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_403_FORBIDDEN)

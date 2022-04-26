from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.serializers import SubscribeCreateSerializer, UserSerializer


class UserCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "subscribe_to_author":
            return SubscribeCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "subscribe_to_author":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["post"], detail=False, url_path="subscribe", url_name="subscribe")
    def subscribe_to_author(self, request):
        return self.create(request)

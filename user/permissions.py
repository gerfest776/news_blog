from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if not isinstance(request.user, AnonymousUser):
            return bool(request.user and request.user.user_role == "author")
        return False

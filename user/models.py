from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        AUTHOR = "author"
        SUBSCRIBER = "subscriber"

    user_role = models.CharField(
        max_length=15,
        choices=UserRole.choices,
    )
    email = models.EmailField(unique=True, max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"


class Subscription(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscribtion_user"
    )
    author = models.ManyToManyField(
        User,
        related_name="subscribtion_authors",
    )

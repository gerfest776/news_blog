from django.contrib.auth.base_user import BaseUserManager
from django.db import IntegrityError, transaction


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        try:
            with transaction.atomic():
                user = self.model(email=self.normalize_email(email), **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except IntegrityError as e:
            raise Exception("User with this email already exists") from e

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password=password, **extra_fields)

"""Custom django user"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import hashers


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        """Create non-admin user"""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self._create(username, email, password, **extra_fields)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self._create(username, email, password, **extra_fields)

        return user

    def _create(self, username, email, password, **extra_fields):
        """Save created user"""

        if not username:
            raise ValueError("Missing username")

        user = self.model(
            username=username, email=email, password=password, **extra_fields
        )
        user.password = hashers.make_password(password)
        user.save()

        return user


class User(AbstractUser):
    """Custom user model"""

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.username}"

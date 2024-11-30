# mypy: disable-error-code="var-annotated"


"""Custom User Model."""

from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Customized User."""

    pkid = models.BigAutoField(
        primary_key=True,
        editable=False,
    )  # Primary key will make sure it's unqiue
    id = models.UUIDField(default=uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=50, verbose_name=_("first name"))
    last_name = models.CharField(max_length=50, verbose_name=_("last name"))
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)

    # By default 'is_superuser' is set to 'False' because of PermissionMixin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        """Return '<user.first_nae> | <user.email>'."""
        return f"{self.first_name} | {self.email}"

    @property
    def full_name(self):
        """Return full name."""
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def short_name(self):
        """Return Capitalized first name."""
        return f"{self.first_name.title()}"

"""Custom user manager."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError as ValidationError_drf

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager.

    Methods
        email_validate
        create_user
        create_superuse

    """

    @staticmethod
    def email_validate(email: str) -> None:
        """
        Validate email.

        Provide custom message "Email provied: %s is invalid. Please provide a valid email." if email is invalid.
        """
        try:
            validate_email(email)

        except ValidationError as CustomUserManager_error:
            raise ValidationError_drf(
                _("Email provied: %s is invalid. Please provide a valid email.")
                % email,
            ) from CustomUserManager_error

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        **extra_fields,
    ) -> AbstractBaseUser:
        """
        Create user.

        Args:
            first_name (str): User first name
            last_name (str): User first last name
            email (str): User email
            password (str): User passwrod
            **extra_fields: other keyword arguments

        Raises:
            ValueError: If one of first_name, last_namem password, email is not provided.

        Returns:
            user(AbstractBaseUser): user instance.

        """
        if not first_name:
            raise ValueError(
                _("User first name is not provided. Please provide a first name."),
            )

        if not last_name:
            raise ValueError(
                _("User last name is not provided. Please provide a last name."),
            )

        if not password:
            raise ValueError(
                _("User passwrod is not provided. Please provide a password."),
            )

        if email:
            email = self.normalize_email(email)
            CustomUserManager.email_validate(email)
        else:
            raise ValueError(
                _("User email is not provided. Please provide an valid email.."),
            )

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        **extra_fields,
    ):
        """
        Create super user.

        Args:
            first_name (str): User's first name
            last_name (str): User's first last name
            email (str): User's email
            password (str): User passwrod
            **extra_fields: other keyword arguments.

        Raises:
            ValueError: If one of 'is_staff' or 'is_superuser' is not set to True.


        Returns:
            user(AbstractBaseUser): user instance.

        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser field: 'is_staff' must be set True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser field: 'is_superuser' must be set True."))

        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields,
        )

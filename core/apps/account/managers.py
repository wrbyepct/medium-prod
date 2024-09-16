from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validate(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(
                _(f"Email provied: {email} is invalid. Please provide a valid email.")
            )

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not first_name:
            raise ValueError(
                _("User first name is not provided. Please provide a first name.")
            )

        if not last_name:
            raise ValueError(
                _("User last name is not provided. Please provide a last name.")
            )

        if not password:
            raise ValueError(
                _("User passwrod is not provided. Please provide a password.")
            )

        if email:
            email = self.normalize_email(email)
            self.email_validate(email)
        else:
            ValueError(_("User email is not provided. Please provide an valid email.."))

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
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

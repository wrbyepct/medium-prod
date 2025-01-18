"""Test model structure."""

import pytest
from django.contrib.auth import get_user_model
from django.db import models


class TestUserModelStructure:
    """Test sets for model fields specifications."""

    model = get_user_model()

    @pytest.mark.parametrize(
        "field_name, field_type",
        [
            ("pkid", models.BigAutoField),
            ("id", models.UUIDField),
            ("first_name", models.CharField),
            ("last_name", models.CharField),
            ("date_joined", models.DateTimeField),
            ("is_active", models.BooleanField),
            ("is_staff", models.BooleanField),
        ],
    )
    def test_user_model_structure_field_type_correct(self, field_name, field_type):
        """Test model field types."""
        assert hasattr(self.model, field_name)

        field = self.model._meta.get_field(field_name)
        assert isinstance(field, field_type)

    @pytest.mark.parametrize(
        "field, constraints",
        [
            ("pkid", [("editable", False)]),
            ("id", [("unique", True)]),
            ("first_name", [("max_length", 50)]),
            ("last_name", [("max_length", 50)]),
            ("email", [("unique", True), ("max_length", 255)]),
            ("date_joined", [("editable", False)]),
            ("is_staff", [("default", False)]),
            ("is_active", [("default", True)]),
        ],
    )
    def test_user_model_structure_constraints_correct(self, field, constraints):
        """Test model field constraints."""
        field = self.model._meta.get_field(field)

        for constraint, expect_value in constraints:
            assert getattr(field, constraint) == expect_value

import pytest
from django.contrib.auth import get_user_model
from django.db import models


class TestUserModelStructure:
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
    def test_model_fields_type(self, field_name, field_type):
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
            ("email", [("unique", True)]),
            ("date_joined", [("editable", False)]),
        ],
    )
    def test_model_constraints(self, field, constraints):
        field = self.model._meta.get_field(field)

        for constraint, expect_value in constraints:
            assert getattr(field, constraint) == expect_value

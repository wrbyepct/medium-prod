import pytest
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.responses.models import Response, ResponseClap

User = get_user_model()


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("response", models.ForeignKey),
        ("user", models.ForeignKey),
    ],
)
def test_response_clap_model__field_type_correct(field_name, field_type):
    assert hasattr(ResponseClap, field_name)

    field = ResponseClap._meta.get_field(field_name)

    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "response",
            [
                ("model", Response),
                ("on_delete", models.CASCADE),
                ("related_name", "claps"),
            ],
        ),
        (
            "user",
            [
                ("model", User),
                ("on_delete", models.CASCADE),
            ],
        ),
    ],
)
def test_response_clap_model_remote_field_constraints_correct(field_name, constraints):
    field = ResponseClap._meta.get_field(field_name)
    remote_field = field.remote_field

    for constraint, value in constraints:
        assert getattr(remote_field, constraint) == value


def test_response_clap_model__meta_constraint_correct():
    meta_cls = ResponseClap._meta
    assert hasattr(meta_cls, "constraints")

    for constraint in meta_cls.constraints:
        assert constraint.fields == ("response", "user")

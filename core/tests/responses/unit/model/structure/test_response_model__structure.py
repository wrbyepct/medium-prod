import pytest
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article
from core.apps.responses.models import Response

User = get_user_model()


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("content", models.TextField),
        ("user", models.ForeignKey),
        ("article", models.ForeignKey),
        ("parent", models.ForeignKey),
    ],
)
def test_response_model__field_type_correct(field_name, field_type):
    assert hasattr(Response, field_name)

    field = Response._meta.get_field(field_name)

    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        ("content", [("blank", True), ("verbose_name", "response content")]),
        ("parent", [("null", True), ("blank", True)]),
    ],
)
def test_response_model__direct_field_contraints_correct(field_name, constraints):
    field = Response._meta.get_field(field_name)

    for constraint, value in constraints:
        assert getattr(field, constraint) == value


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "user",
            [
                ("model", User),
                ("on_delete", models.CASCADE),
            ],
        ),
        (
            "article",
            [
                ("model", Article),
                ("on_delete", models.CASCADE),
                ("related_name", "responses"),
            ],
        ),
        (
            "parent",
            [
                ("model", Response),
                ("on_delete", models.CASCADE),
                ("related_name", "children"),
            ],
        ),
    ],
)
def test_response_model__remote_field_contraints_correct(field_name, constraints):
    field = Response._meta.get_field(field_name)

    remote_field = field.remote_field
    for constraint, value in constraints:
        assert getattr(remote_field, constraint) == value

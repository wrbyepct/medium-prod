import pytest
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article, Clap

User = get_user_model()


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("article", models.ForeignKey),
        ("user", models.ForeignKey),
    ],
)
def test_article_clap_model__field_type_correct(field_name, field_type):
    assert hasattr(Clap, field_name)

    field = Clap._meta.get_field(field_name)
    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "article",
            [
                ("model", Article),
                ("on_delete", models.CASCADE),
                ("related_name", "claps"),
            ],
        ),
        ("user", [("model", User), ("on_delete", models.CASCADE)]),
    ],
)
def test_article_clap_model__field_constraints_correct(field_name, constraints):
    field = Clap._meta.get_field(field_name)

    for attr, value in constraints:
        assert getattr(field.remote_field, attr) == value

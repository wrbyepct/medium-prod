import pytest
from django.db import models

from core.apps.articles.models import ArticleView


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("article", models.ForeignKey),
        ("user", models.ForeignKey),
        ("viewer_ip", models.GenericIPAddressField),
    ],
)
def test_article_view_model__field_type_correct(field_name, field_type):
    assert hasattr(ArticleView, field_name)

    field = ArticleView._meta.get_field(field_name)
    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        ("article", [("on_delete", models.CASCADE), ("related_name", "article_views")]),
        (
            "user",
            [
                ("on_delete", models.SET_NULL),
                ("null", True),
                ("related_name", "articles_viewed"),
            ],
        ),
        ("viewer_ip", [("null", True), ("blank", True)]),
    ],
)
def test_article_view_model__field_constraints_correct(field_name, constraints):
    field = ArticleView._meta.get_field(field_name)

    for attr, value in constraints:
        # Handle 'on_delete' separately
        if attr == "on_delete":
            assert field.remote_field.on_delete == value

        # Handle 'related_name' separately
        elif attr == "related_name":
            assert field.remote_field.related_name == value

        else:
            # default case: direct attribute on 'field'
            assert getattr(field, attr) == value

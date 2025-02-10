import pytest
from django.contrib.auth import get_user_model
from django.db import models

from core.apps.articles.models import Article
from core.apps.ratings.models import Rating

User = get_user_model()


# test model field type corrects
@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("rating", models.PositiveSmallIntegerField),
        ("review", models.TextField),
        ("user", models.ForeignKey),
        ("article", models.ForeignKey),
    ],
)
def test_rating_model_structure__field_type_correct(field_name, field_type):
    assert hasattr(Rating, field_name)

    field = Rating._meta.get_field(field_name)
    assert isinstance(field, field_type)


# test model field  constraints correct
@pytest.mark.parametrize(
    "field_name, constraints",
    [
        ("rating", [("choices", Rating.RATING_CHOICES)]),
        ("review", [("blank", True)]),
    ],
)
def test_rating_model_structure__direct_field_constraints_correct(
    field_name, constraints
):
    field = Rating._meta.get_field(field_name)

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
                ("related_name", "ratings"),
            ],
        ),
    ],
)
def test_rating_model_structure__remote_field_constraints_correct(
    field_name, constraints
):
    field = Rating._meta.get_field(field_name)

    remote_field = field.remote_field

    for constraint, value in constraints:
        assert getattr(remote_field, constraint) == value


def test_rating_model__unique_constraint_correct():
    meta_cls = Rating._meta
    assert hasattr(meta_cls, "constraints")
    constraints = meta_cls.constraints

    assert len(constraints) == 1, constraints
    assert constraints[0].fields == ("article", "user")
    assert constraints[0].name == "unqiue_rating_per_article_and_user"

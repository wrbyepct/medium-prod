import pytest
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from core.apps.articles.models import Article
from core.apps.bookmarks.models import BookmarksInCategories, ReadingCategory
from core.tools.hash import generate_hashed_slug

User = get_user_model()


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("title", models.CharField),
        ("slug", AutoSlugField),
        ("description", models.TextField),
        ("is_private", models.BooleanField),
        ("is_reading_list", models.BooleanField),
        ("user", models.ForeignKey),
        ("bookmarks", models.ManyToManyField),
    ],
)
def test_bookmark_category_model_structure__field_type_correct(field_name, field_type):
    assert hasattr(ReadingCategory, field_name)

    field = ReadingCategory._meta.get_field(field_name)

    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "title",
            [
                ("validators", [MinLengthValidator(1), MaxLengthValidator(60)]),
                ("max_length", 60),
            ],
        ),
        (
            "slug",
            [
                ("populate_from", generate_hashed_slug),
                ("always_update", True),
                ("unique", True),
            ],
        ),
        (
            "description",
            [
                ("blank", True),
            ],
        ),
        (
            "is_private",
            [
                ("default", False),
            ],
        ),
        (
            "is_reading_list",
            [
                ("default", False),
            ],
        ),
    ],
)
def test_bookmark_category_model_structure__direct_field_constraints_correct(
    field_name, constraints
):
    field = ReadingCategory._meta.get_field(field_name)

    for constraint, value in constraints:
        assert getattr(field, constraint) == value


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "bookmarks",
            [
                ("model", Article),
                ("through", BookmarksInCategories),
            ],
        ),
        (
            "user",
            [
                ("model", User),
                ("on_delete", models.CASCADE),
                ("related_name", "reading_categories"),
            ],
        ),
    ],
)
def test_bookmark_category_model_structure__remote_field_constraints_correct(
    field_name, constraints
):
    field = ReadingCategory._meta.get_field(field_name)

    remote_field = field.remote_field
    for constraint, value in constraints:
        assert getattr(remote_field, constraint) == value

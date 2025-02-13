import pytest
from django.db import models

from core.apps.articles.models import Article
from core.apps.bookmarks.models import BookmarksInCategories, ReadingCategory


# type correct
@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("category", models.ForeignKey),
        ("bookmark", models.ForeignKey),
    ],
)
def test_bookmarks_through_table__field_type_correct(field_name, field_type):
    assert hasattr(BookmarksInCategories, field_name)

    field = BookmarksInCategories._meta.get_field(field_name)

    assert isinstance(field, field_type)


# remote constraint
@pytest.mark.parametrize(
    "field_name, constraints",
    [
        (
            "category",
            [
                ("model", ReadingCategory),
                ("on_delete", models.CASCADE),
            ],
        ),
        (
            "bookmark",
            [
                ("model", Article),
                ("on_delete", models.CASCADE),
            ],
        ),
    ],
)
def test_bookmarks_through_table__remote_field_constraint_correct(
    field_name, constraints
):
    field = BookmarksInCategories._meta.get_field(field_name)
    remote_field = field.remote_field
    for constraint, value in constraints:
        assert getattr(remote_field, constraint) == value


# meta constraint
def test_bookmarks_through_table__unique_constraint_correct():
    constraints = BookmarksInCategories._meta.constraints

    assert len(constraints) == 1
    unique_constraint = constraints[0]

    assert unique_constraint.fields == ("category", "bookmark")
    assert unique_constraint.name == "unique_boomark_per_category"

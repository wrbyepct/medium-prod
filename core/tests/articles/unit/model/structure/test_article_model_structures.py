from uuid import uuid4

import pytest
from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core.apps.articles.models import Article
from core.tools.hash import generate_hashed_slug


@pytest.mark.parametrize(
    "field_name, field_type",
    [
        ("pkid", models.BigAutoField),
        ("id", models.UUIDField),
        ("created_at", models.DateTimeField),
        ("updated_at", models.DateTimeField),
        ("title", models.CharField),
        ("description", models.CharField),
        ("body", models.TextField),
        ("banner_image", models.ImageField),
        ("slug", AutoSlugField),
        ("author", models.ForeignKey),
        ("tags", TaggableManager),
    ],
)
def test_article_model_structure__field_type_correct(field_name, field_type):
    assert hasattr(Article, field_name)
    field = Article._meta.get_field(field_name)
    assert isinstance(field, field_type)


@pytest.mark.parametrize(
    "field_name, constraints",
    [
        ("pkid", [("primary_key", True)]),
        ("id", [("default", uuid4), ("editable", False), ("unique", True)]),
        ("created_at", [("auto_now_add", True), ("editable", False)]),
        ("updated_at", [("auto_now", True)]),
        ("title", [("verbose_name", _("Title")), ("max_length", 255)]),
        (
            "description",
            [("verbose_name", _("Description")), ("max_length", 255), ("blank", True)],
        ),
        ("body", [("verbose_name", _("article content"))]),
        (
            "banner_image",
            [("verbose_name", _("Banner Image")), ("null", True), ("blank", True)],
        ),
        (
            "slug",
            [
                ("populate_from", generate_hashed_slug),
                ("always_update", True),
                ("unique", True),
                ("max_length", 300),
            ],
        ),
    ],
)
def test_article_model_structure__field_contraints_correct(field_name, constraints):
    field = Article._meta.get_field(field_name)

    for attr, val in constraints:
        assert getattr(field, attr) == val

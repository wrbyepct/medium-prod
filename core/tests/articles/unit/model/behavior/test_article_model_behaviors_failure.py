import pytest
from django.db.utils import DataError

pytestmark = pytest.mark.django_db


def test_article_model_behavior__title_exceeding_255_create_fail(article_factory):
    title = "a" * 256
    with pytest.raises(DataError):
        article_factory.create(title=title)


def test_article_model_behavior__description_exceeding_255_create_fail(article_factory):
    description = "a" * 256
    with pytest.raises(DataError):
        article_factory.create(description=description)

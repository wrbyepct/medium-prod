import pytest
from django.db import IntegrityError

from core.apps.bookmarks.models import ReadingCategory

pytestmark = pytest.mark.django_db


# model create successufl & str method
def test_reading_category__model_create_corrent(reading_category_factory, normal_user):
    bookmarks_num = 3

    cate_data = {"title": "Test cate", "description": "Test", "user": normal_user}

    cate = reading_category_factory.create(with_bookmarks=bookmarks_num, **cate_data)

    assert cate.title == cate_data["title"]
    assert cate.description == cate_data["description"]
    assert cate.user == cate_data["user"]
    assert cate.slug is not None
    assert not cate.is_private
    assert not cate.is_reading_list
    assert cate.bookmarks.count() == bookmarks_num

    assert (
        cate.__str__()
        == f"User: {normal_user.first_name} {normal_user.last_name}'s Bookmark category: {cate.title}."
    )


# add the same article has no effect
def test_reading_category_model__add_same_article_raise_integrity_error(
    reading_category_factory, article
):
    cate = reading_category_factory.create()
    cate.bookmarks.add(article)
    assert cate.bookmarks.count() == 1

    cate.bookmarks.add(article)
    assert cate.bookmarks.count() == 1


# create without user raise error
def test_reading_category_model__create_without_user_raise_integrity_error():
    cate_data = {"title": "Test cate", "description": "Test"}

    with pytest.raises(IntegrityError):
        ReadingCategory.objects.create(**cate_data)


def test_reading_category_model__delete_associated_user_cascade(
    reading_category_factory,
):
    cate = reading_category_factory.create()
    assert ReadingCategory.objects.filter(id=cate.id).exists()

    # Act
    user = cate.user
    user.delete()

    assert not ReadingCategory.objects.filter(id=cate.id).exists()


def test_reading_category_model__slug_unique(reading_category_factory):
    title = "Test Title"
    cate1 = reading_category_factory.create(title=title)
    cate2 = reading_category_factory.create(title=title)

    assert cate1.slug != cate2.slug

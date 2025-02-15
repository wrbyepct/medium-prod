import pytest
from django.db import IntegrityError

from core.apps.bookmarks.models import BookmarksInCategories

pytestmark = pytest.mark.django_db


def test_bookmark_in_category__model_create_successful(bookmark_in_category_factory):
    bookmark = bookmark_in_category_factory.create()

    cate = bookmark.category
    user = cate.user
    article = bookmark.bookmark

    assert cate is not None
    assert article is not None

    assert (
        bookmark.__str__()
        == f"Article: {article.title} in user: {user.full_name}'s list: {cate.title}."
    )


# category delete cascade correct
def test_bookmark_in_category__associated_article_delete_cascade(
    bookmark_in_category_factory, mock_article_index_delete
):
    bookmark = bookmark_in_category_factory.create()
    article = bookmark.bookmark

    assert BookmarksInCategories.objects.filter(id=bookmark.id).exists()

    # Act
    article.delete()

    # Assert
    assert not BookmarksInCategories.objects.filter(id=bookmark.id).exists()


# article delete cascade correct


def test_bookmark_in_category__associated_category_delete_cascade(
    bookmark_in_category_factory,
):
    bookmark = bookmark_in_category_factory.create()
    cate = bookmark.category

    assert BookmarksInCategories.objects.filter(id=bookmark.id).exists()

    # Act
    cate.delete()

    # Assert
    assert not BookmarksInCategories.objects.filter(id=bookmark.id).exists()


# violate unique constraint raise integrity error
def test_bookmark_in_category__unique_constraint_with_category_bookmark(
    bookmark_in_category_factory, reading_category_factory, article
):
    cate = reading_category_factory.create()

    bookmark_in_category_factory.create(category=cate, bookmark=article)

    with pytest.raises(IntegrityError):
        bookmark_in_category_factory.create(category=cate, bookmark=article)

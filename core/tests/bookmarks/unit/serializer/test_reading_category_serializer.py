from uuid import uuid4

import pytest
from dateutil.parser import isoparse
from django.http import Http404
from rest_framework import serializers

from core.apps.bookmarks.models import ReadingCategory
from core.apps.bookmarks.serializers import (
    DynamicPrimaryKeyRelatedField,
    ReadingCategorySerializer,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def valid_data():
    return {
        "title": "test A",
        "description": "test B",
        "is_private": True,
    }


"""
Serialize
"""


def test_reading_category_serializer__serialize_correct(reading_category_factory):
    """Test ReadingCategorySerializer serialize correctly."""

    cate = reading_category_factory.create()
    cate = ReadingCategory.objects.get(id=cate.id)

    serializer = ReadingCategorySerializer(cate)

    fields = [
        "slug",
        "title",
        "description",
        "is_private",
        # no category field, popped out in representation
        "bookmarks_count",
    ]

    for field in fields:
        assert field in serializer.data
        assert serializer.data[field] == getattr(cate, field)

    assert "updated_at" in serializer.data
    assert isoparse(serializer.data["updated_at"]) == cate.updated_at

    assert "id" in serializer.data
    assert serializer.data["id"] == str(cate.id)

    assert "bookmarks" in serializer.data
    assert len(serializer.data["bookmarks"]) == cate.bookmarks.count()


def test_reading_category__category_field_return_ones_belonged_to_user(
    normal_user, reading_category_factory, mocker
):
    """Test DynamicPrimaryKeyRelatedField return user's existing category instances."""
    # Arrange: given 6 existing categories, 3 belong to normal user; 3 are not
    size = 3
    reading_category_factory.create_batch(size=size, user=normal_user)
    reading_category_factory.create_batch(size=size)

    base_qs = ReadingCategory.objects.all()
    user_cates = base_qs.filter(user=normal_user)

    # Arrange: use dummy serializer to pass in context(only serializer can accept context)
    class DummySerializer(serializers.Serializer):
        category = DynamicPrimaryKeyRelatedField(
            queryset=base_qs,
            allow_null=True,
            required=False,
        )

    mock_request = mocker.Mock(user=normal_user)
    serializer = DummySerializer(
        data={},
        context={"request": mock_request},
    )

    # Act
    field = serializer.fields["category"]
    qs = field.get_queryset()

    assert qs.count() == user_cates.count()
    for result, expected in zip(qs, user_cates):
        assert result == expected


"""
Deserialize
"""


def test_reading_category_serializer__valid_data_deserialize_correct(
    valid_data, article, normal_user
):
    """Test ReadingCategorySerializer valid data deserialize correctly."""

    serializer = ReadingCategorySerializer(
        data=valid_data, context={"article_id": article.id}
    )

    assert serializer.is_valid()
    assert serializer.validated_data == valid_data

    # Act
    validated_data = serializer.validated_data
    validated_data["user"] = normal_user
    cate = serializer.create(validated_data)

    # Assert saveed data
    assert cate.user == validated_data["user"]
    assert article in cate.bookmarks.all()
    assert cate.title == validated_data["title"]
    assert cate.description == validated_data["description"]
    assert cate.is_private == validated_data["is_private"]


def test_reading_category_serializer__handle_article_adding__if_article_id_present_then_add_correct(
    article, reading_category_factory
):
    # Arrange: given serializer with article_id in context
    serializer = ReadingCategorySerializer(context={"article_id": article.id})
    # Arrange: givne an existing category
    category = reading_category_factory.create()

    # Act
    serializer.handle_article_adding(category)
    category.refresh_from_db()

    # Assert
    assert article in category.bookmarks.all()


# article id not found
def test_reading_category_serializer__handle_article_adding__if_article_id_not_found_then_raise_404(
    reading_category_factory,
):
    # Arrange: given serializer with non-existing article_id in context
    serializer = ReadingCategorySerializer(context={"article_id": uuid4()})
    # Arrange: givne an existing category
    category = reading_category_factory.create()

    # Act
    with pytest.raises(Http404):
        serializer.handle_article_adding(category)

    # Assert
    category.refresh_from_db()
    assert category.bookmarks.count() == 0


# no id, bookmark is not added
def test_reading_category_serializer__handle_article_adding__if_no_article_id_then_no_effect(
    reading_category_factory,
):
    # Arrange: given serializer with non-existing article_id in context
    serializer = ReadingCategorySerializer()
    # Arrange: givne an existing category
    category = reading_category_factory.create()

    # Act
    serializer.handle_article_adding(category)
    category.refresh_from_db()

    # Assert
    assert category.bookmarks.count() == 0


def test_reading_category_serializer__update_method_with_non_default_category_correct(
    reading_category_factory, normal_user, valid_data
):
    user_cate = reading_category_factory.create(user=normal_user)

    validated_data = valid_data

    serializer = ReadingCategorySerializer()
    updated_cate = serializer.update(user_cate, validated_data)

    assert updated_cate.title == validated_data["title"]
    assert updated_cate.description == validated_data["description"]
    assert updated_cate.is_private == validated_data["is_private"]
    assert updated_cate.user == normal_user


# update method do not update default reading list title
def test_reading_category_serializer__update_method_do_not_update_default_reading_list_title(
    reading_category_factory, valid_data
):
    validated_data = valid_data.copy()  # dict is mutable
    reading_list = reading_category_factory.create(is_reading_list=True)

    serializer = ReadingCategorySerializer()
    updated_reading_list = serializer.update(reading_list, validated_data)

    assert updated_reading_list.title != valid_data["title"]
    assert updated_reading_list.description == valid_data["description"]
    assert updated_reading_list.is_private == valid_data["is_private"]

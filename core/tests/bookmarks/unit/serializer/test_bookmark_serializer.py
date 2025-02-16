import pytest

from core.apps.articles.models import Article
from core.apps.bookmarks.serializers import (
    PARTIAL_ARITCLE_BODY_MAX_LENGTH,
    BookmarkSerializer,
)

pytestmark = pytest.mark.django_db


"""
Serialize
"""


# serialize data correct
def test_bookmark_serializer__serialize_correct(article):
    article = Article.statistic_objects.preview_data().get(id=article.id)
    fields = [
        "title",
        "claps_count",
        "responses_count",
    ]
    serializer = BookmarkSerializer(article)

    for field in fields:
        assert field in serializer.data
        assert serializer.data[field] == getattr(article, field)

    assert "banner_image" in serializer.data
    assert serializer.data["banner_image"] is None

    assert "created_at" in serializer.data
    field = serializer.fields["created_at"]
    assert serializer.data["created_at"] == field.to_representation(article.created_at)

    assert "id" in serializer.data
    assert serializer.data["id"] == str(article.id)

    assert "partial_body" in serializer.data
    assert serializer.data["partial_body"] == serializer.get_partial_body(article)


# partial_body method correct
@pytest.mark.parametrize(
    "text, expected_len",
    [
        ("a" * (PARTIAL_ARITCLE_BODY_MAX_LENGTH + 1), PARTIAL_ARITCLE_BODY_MAX_LENGTH),
        ("a" * 123, 123),
    ],
)
def test_bookmark_serializer__handle_text_length_correct(text, expected_len):
    serializer = BookmarkSerializer()

    output_text = serializer._handle_text_length(text)

    assert len(output_text) == expected_len


"""
No deserializing to test, BookmarkSerializer is read-only
"""

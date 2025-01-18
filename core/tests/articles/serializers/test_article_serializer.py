import pytest

from core.apps.articles.models import Article
from core.apps.articles.serializers import (
    ArticleSerializer,
    ClapSerializer,
    TagListField,
)
from core.apps.profiles.models import Profile
from core.apps.profiles.serializers import ProfileSerializer

pytestmark = pytest.mark.django_db


# Test serialize corect


def test_article_serializer__serialize_successful(article):
    article = Article.statistic_objects.get(pk=article.pk)
    serializer = ArticleSerializer(article)

    for field in ArticleSerializer.Meta.fields:
        assert field in serializer.data


@pytest.mark.parametrize(
    "field",
    [
        "slug",
        "title",
        "description",
        "body",
        "estimated_reading_time",
        "avg_rating",
        "claps_count",
        "views",
        "responses_count",
    ],
)
def test_article_serializer__serialize_simple_fields_data_correct(article, field):
    article = Article.statistic_objects.get(pk=article.pk)
    serializer = ArticleSerializer(article)
    assert getattr(article, field) == serializer.data[field]


def test_article_serializer__serialize_complex_fields_data_correct(article):
    # Arrange
    profile = Profile.objects.create(user=article.author)
    article.refresh_from_db()

    # Act
    serializer = ArticleSerializer(article)

    assert serializer.data["id"] == str(article.id)
    assert serializer.data["banner_image"] == "No image"
    assert serializer.data["created_at"] == article.created_at.strftime(
        "%m/%d/%Y, %H:%M:%S"
    )
    assert serializer.data["updated_at"] == article.updated_at.strftime(
        "%m/%d/%Y, %H:%M:%S"
    )

    tags = TagListField().to_representation(article.tags)
    assert serializer.data["tags"] == tags

    clap_serializer = ClapSerializer(article.claps, many=True)
    assert serializer.data["clapped_by"] == clap_serializer.data

    profile_serializer = ProfileSerializer(profile)
    assert serializer.data["author_info"] == profile_serializer.data


# Test deserialize correct


# Test create


# Test update


# Test to_representation

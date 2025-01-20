import json
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
def test_article_serializer__deserialize_valid_data_successful(mock_image_upload):
    valid_info = {
        "title": "Test Title",
        "description": "Test body",
        "body": "Test body",
        "tags": '["A", "B"]',
        "banner_image": mock_image_upload,
    }
    serializer = ArticleSerializer(data=valid_info)

    assert serializer.is_valid()

    data = serializer.validated_data

    assert "title" in data
    assert "description" in data
    assert "body" in data
    assert "tags" in data
    assert "banner_image" in data

    assert data["title"] == valid_info["title"]
    assert data["description"] == valid_info["description"]
    assert data["body"] == valid_info["body"]
    assert data["tags"] == json.loads(valid_info["tags"])
    assert data["banner_image"] == valid_info["banner_image"]


def test_article_serializer__deserialize_read_only_fields_no_effect():
    data_info = {
        "title": "Test Title",
        "description": "Test body",
        "body": "Test body",
        # Read onl fields
        "estimated_reading_time": 1,
        "avg_rating": 1,
        "views": 1,
        "responses_count": 1,
        "claps_count": 1,
        "clapped_by": "James",
        "author_info": "James",
        "created_at": 1,
        "updated_at": 1,
    }

    serializer = ArticleSerializer(data=data_info)

    assert serializer.is_valid(), serializer.errors
    data = serializer.validated_data

    read_only_fields = [
        "estimated_reading_time",
        "avg_rating",
        "views",
        "responses_count",
        "claps_count",
        "clapped_by",
        "created_at",
        "updated_at",
        "author_info",
    ]
    for field in read_only_fields:
        assert field not in data


# Test serializer.create()
def test_article_serializer__create_return_article_correct(
    normal_user, mock_article_index_update
):
    valid_info = {
        "title": "Test Title",
        "description": "Test body",
        "body": "Test body",
    }

    serializer = ArticleSerializer(data=valid_info)

    assert serializer.is_valid(), serializer.errors

    data = serializer.validated_data
    data["author"] = normal_user

    article = serializer.create(data)
    assert article.title == valid_info["title"]
    assert article.description == valid_info["description"]
    assert article.body == valid_info["body"]
    assert article.author == normal_user
    assert article.tags.all().count() == 0
    assert article.banner_image.name is None


# Test erializer.update()
def test_article_serializer__update_article_correct(
    article, mock_image_upload, mock_media_dir, mock_article_index_update
):
    # Arrane
    update_info = {
        "title": "Test Title New",
        "description": "Test body New",
        "body": "Test body New",
        "banner_image": mock_image_upload,
        "tags": '["C", "D"]',
    }

    old_update_time = article.updated_at

    # Act
    serializer = ArticleSerializer(data=update_info)
    assert serializer.is_valid(), serializer.errors

    article_updated = serializer.update(
        instance=article, validated_data=serializer.validated_data
    )

    # Assert
    assert article_updated.title == update_info["title"]
    assert article_updated.description == update_info["description"]
    assert article_updated.body == update_info["body"]

    assert article_updated.banner_image.name == update_info["banner_image"].name
    assert list(article_updated.tags.values_list("name", flat=True)) == json.loads(
        update_info["tags"]
    )
    assert article_updated.updated_at != old_update_time

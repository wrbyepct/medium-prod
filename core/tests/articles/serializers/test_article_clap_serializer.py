import pytest

from core.apps.articles.serializers import ClapSerializer

pytestmark = pytest.mark.django_db


def test_article_clap_seializer__serialize_fields_correct(article_clap_factory):
    clap = article_clap_factory.create()

    serializer = ClapSerializer(clap)

    assert "user_name" in serializer.data
    assert clap.user.full_name == serializer.data["user_name"]

    assert "created_at" in serializer.data
    assert (
        clap.created_at.strftime("%m/%d/%Y, %H:%M:%S") == serializer.data["created_at"]
    )


def test_article_clap_seializer__deserialize_fields_not_writable():
    from datetime import datetime

    clap_data = {
        "user_name": "TestMan",
        "created_at": datetime.now(),
    }
    serializer = ClapSerializer(data=clap_data)
    serializer.is_valid()

    assert "user_name" not in serializer.validated_data
    assert "created_at" not in serializer.validated_data

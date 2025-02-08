import pytest

from core.apps.responses.models import Response
from core.apps.responses.serializers import ResponseSerializer

pytestmark = pytest.mark.django_db

resp_fields = [
    "id",
    "user_full_name",
    "content",
    "article",
    "parent",
    "claps_count",
    "replies_count",
    "created_at",
]

read_only_fields = [
    "article",
    "parent",
    "created_at",
]


def test_response_serializer__serilaize_correct(response_factory):
    # Arrange
    response = response_factory.create()
    response = Response.objects.get(id=response.id)

    user = response.user

    # Act
    serializer = ResponseSerializer(response)
    for field in resp_fields:
        assert field in serializer.data

    assert serializer.get_user_full_name(response) == user.full_name


def test_response_serializer__deserilaize_correct(user_factory, article_factory):
    user = user_factory.create()
    article = article_factory.create()
    response_data = {"content": "test context"}

    # Assert:  serilaizer data correct
    serializer = ResponseSerializer(data=response_data)
    assert serializer.is_valid(), serializer.errors

    # Assert: serializer save data correct
    serializer.save(user=user, article=article)
    response = Response.objects.filter(user=user, article=article)

    assert response.exists()
    assert response.count() == 1
    assert response[0].content == response_data["content"]

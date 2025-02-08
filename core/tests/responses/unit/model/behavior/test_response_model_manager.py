import pytest

from core.apps.responses.models import Response

pytestmark = pytest.mark.django_db


def test_response_model__has_annotated_fields(response_factory):
    response = response_factory.create()

    response = Response.objects.get(id=response.id)

    expected_fields = {
        "id",
        "content",
        "created_at",
        "claps_count",
        "replies_count",
        "article_id",
        "parent_id",
        "user_id",
    }
    response_fields = set(response.__dict__.keys())

    for field in expected_fields:
        assert field in response_fields

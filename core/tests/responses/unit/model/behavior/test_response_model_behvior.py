import pytest
from django.contrib.auth import get_user_model

from core.apps.articles.models import Article
from core.apps.responses.models import Response

pytestmark = pytest.mark.django_db
# test Response Custom Manager


User = get_user_model()

# Test Response method


def test_response_model__create_instance_success(response_factory):
    res_children_size = 3
    response = response_factory.create(
        with_children=res_children_size,
        with_parent=True,
    )

    assert response.user is not None
    assert isinstance(response.user, User)

    assert response.article is not None
    assert isinstance(response.article, Article)

    assert response.children.count() == res_children_size
    assert isinstance(response.parent, Response)
    assert (
        response.__str__()
        == f"User: {response.user.full_name}'s response to article: {response.article.title}"
    )


# Test ResponseClap


def test_response_clap_model__create_instance_success(response_clap_factory):
    response_clap = response_clap_factory.create()

    assert response_clap.user is not None
    assert isinstance(response_clap.user, User)

    assert response_clap.response is not None
    assert isinstance(response_clap.response, Response)
    assert (
        response_clap.__str__()
        == f"User: {response_clap.user.full_name} clapped the response by {response_clap.response.user.full_name}."
    )

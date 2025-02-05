import pytest
from django.db import IntegrityError
from rest_framework import status

from core.apps.articles.models import Article, Clap
from core.apps.articles.views import ClapCreateDestroyView

pytestmark = pytest.mark.django_db


@pytest.fixture
def article_clap_mocks(article_factory, mocker):
    article = article_factory.build()
    return {
        "article": article,
        "clap": mocker.patch("core.apps.articles.views.Clap"),
        "get_object_or_404": mocker.patch(
            "core.apps.articles.views.get_object_or_404", return_value=article
        ),
    }


def clap_create_cases():
    return [
        (
            None,
            status.HTTP_201_CREATED,
            lambda article: f"Successfully clapped the article: {article.title}",
        ),
        (
            IntegrityError,  # simulate raising IntegrityError during create()
            status.HTTP_400_BAD_REQUEST,
            lambda article: "You already clapped the article",
        ),
    ]


@pytest.mark.parametrize(
    "clap_create_side_effect, expected_status_code, expected_message",
    clap_create_cases(),
)
def test_article_clap__create(
    mocker,
    api_request_with_user,
    article_clap_mocks,
    clap_create_side_effect,
    expected_status_code,
    expected_message,
):
    # Given mock request return a fake user
    request = api_request_with_user()

    mocks = article_clap_mocks
    # Patch Clap and get_object_or_404
    mocks["clap"].objects.create.side_effect = clap_create_side_effect

    # Act
    view = ClapCreateDestroyView()
    response = view.post(request, mocks["article"].id)

    # Assert
    mocks["get_object_or_404"].assert_called_once_with(
        mocker.ANY, id=mocks["article"].id
    )
    mocks["clap"].objects.create.assert_called_once_with(
        user=request.user, article=mocks["article"]
    )
    assert response.status_code == expected_status_code
    assert response.data["message"] == expected_message(mocks["article"])


def test_article_clap__destory(mocker, api_request_with_user):
    # Setup mocks
    request = api_request_with_user()
    article = "fake_article"
    clap = mocker.Mock()

    def side_effect(model, *args, **kwargs):
        if model == Article:
            return article
        return clap

    mock_get_object_or_404 = mocker.patch(
        "core.apps.articles.views.get_object_or_404", side_effect=side_effect
    )
    article_id = "fake_article_id"

    # Act
    view = ClapCreateDestroyView()
    response = view.delete(request, article_id)

    # Assert
    mock_get_object_or_404.assert_any_call(
        Article,
        id=article_id,
    )
    mock_get_object_or_404.assert_any_call(
        Clap,
        user=request.user,
        article=article,
    )
    clap.delete.assert_called_once()
    assert response.status_code == status.HTTP_200_OK

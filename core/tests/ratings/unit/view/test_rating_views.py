from uuid import uuid4

import pytest
from django.http import Http404
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from core.apps.ratings.exceptions import YouCannotRateArticleAgain
from core.apps.ratings.views import RatingCreateListView

pytestmark = pytest.mark.django_db


# test rating list create view methods: get_queryset
def get_endpoint(article_id):
    return reverse("article_ratings_list_create", args=[article_id])


class TestRatingListCreateView:
    def test_get_queryset_correct_when_article_exists(self, mocker, article):
        # Arrange: given view with a request and article_id
        request = APIRequestFactory().get("/")
        view = RatingCreateListView()
        view.setup(request, article_id=article.id)

        # Arrange: patch rating model
        mock_rating = mocker.patch("core.apps.ratings.views.Rating")

        # Act: call get_queryset
        view.get_queryset()

        # Assert mock rating call filter correctly
        mock_rating.objects.filter.assert_called_once_with(article=article)

    # mocck get_object or 404 called correctly
    def test_get_queryset_raise_http404_when_article_not_exist(self, mocker, article):
        # Arrange: given view with a request

        request = APIRequestFactory().get("/")
        view = RatingCreateListView()
        view.setup(request, article_id=uuid4())

        with pytest.raises(Http404):
            view.get_queryset()

    def test_perform_create_correct(self, mocker, article, normal_user):
        # Arrange: Preapre view
        request = APIRequestFactory().get("/")
        request.user = normal_user
        view = RatingCreateListView()
        view.setup(request, article_id=article.id)

        # Arrange: mock Rating serializer
        mock_serializer = mocker.Mock()

        # Act
        view.perform_create(mock_serializer)

        # Assert: serializer .save() get called
        mock_serializer.save.assert_called_once_with(user=normal_user, article=article)

    def test_perform_create_repeating_create_raise_error(
        self, mocker, article, normal_user, rating_factory
    ):
        # Arrange: given an existing rating with normal user and default article
        rating_factory.create(user=normal_user, article=article)

        request = APIRequestFactory().get("/")
        request.user = normal_user

        view = RatingCreateListView()
        view.setup(request, article_id=article.id)

        # Arrange: mock Rating serializer
        mock_serializer = mocker.Mock()

        with pytest.raises(YouCannotRateArticleAgain):
            view.perform_create(mock_serializer)

from functools import partial
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.ratings.models import Rating
from core.apps.ratings.serializers import RatingSerializer

pytestmark = pytest.mark.django_db


def get_endpoint(article_id):
    return reverse("article_ratings_list_create", args=[article_id])


def get_randint_list(size: int) -> list:
    import random

    return [random.randint(1, 5) for _ in range(size)]


def _get_expected_stats(value: int, value_list: list):
    return {
        "exact": value_list.count(value),
        "gte": sum(1 for x in value_list if x >= value),
        "lte": sum(1 for x in value_list if x <= value),
    }


def get_filter_queries(term: str, ratings: list):
    """Return list of pairs: (query_param, expected_count)."""
    exact = "exact"
    lte = "lte"
    gte = "gte"
    expected_stats = partial(_get_expected_stats, value_list=ratings)
    return [
        # Exact
        ({term: 5}, expected_stats(5)[exact]),
        ({term: 2}, expected_stats(2)[exact]),
        ({term: 1}, expected_stats(1)[exact]),
        # Less than and equal to
        ({f"{term}__{lte}": 5}, expected_stats(5)[lte]),
        ({f"{term}__{lte}": 2}, expected_stats(2)[lte]),
        ({f"{term}__{lte}": 1}, expected_stats(1)[lte]),
        # Greater than and equal to
        ({f"{term}__{gte}": 5}, expected_stats(5)[gte]),
        ({f"{term}__{gte}": 2}, expected_stats(2)[gte]),
        ({f"{term}__{gte}": 1}, expected_stats(1)[gte]),
    ]


class TestRatingListEndpoint:
    # test unauth get 401
    def test_unauthed_get_401(self, client, article):
        endpoint = get_endpoint(article.id)
        resp = client.get(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # test list get 200 and data correct
    def test_authed_get_200_and_data_corect(
        self, authenticated_client, rating_factory, article
    ):
        rating_count = 3
        # Arrange: given an article with 3 ratings
        rating_factory.create_batch(article=article, size=rating_count)

        # Act
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.get(endpoint)

        # Assert: assert code and data correct
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == rating_count

        ratings = Rating.objects.filter(article=article).order_by(
            "-rating", "-created_at"
        )
        serializer = RatingSerializer(ratings, many=True)

        assert resp.data["results"] == serializer.data

    # test non-existing article

    def test_provide_non_existing_article_get_404(self, authenticated_client):
        endpoint = get_endpoint(uuid4())

        resp = authenticated_client.get(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # test valid ordering filter query correct
    def test_valid_odering_query_correct(
        self, rating_factory, article, authenticated_client
    ):
        # Arrange: given 3 ratings of an article
        ratings_size = 3
        rating_factory.create_batch(article=article, size=ratings_size)
        queries = ["created_at", "-created_at", "rating", "-rating"]
        endpoint = get_endpoint(article.id)

        for query in queries:
            query_term = {"ordering": query}

            resp = authenticated_client.get(endpoint, data=query_term)
            assert resp.status_code == status.HTTP_200_OK

            # Assert: request result is the same as manual ordered results
            ratings = Rating.objects.filter(article=article).order_by(query)
            serializer = RatingSerializer(ratings, many=True)
            assert resp.data["results"] == serializer.data

    # test invalid  ordering query no effect

    def test_invalid_odering_query_no_effect(
        self, rating_factory, article, authenticated_client, user_factory
    ):
        """
        Given rating instances with the order of A(r:3), B(r:2), C(r:1), r is rating.
        By default it will be sorted by rating: default results will be A, B, C
        If I sort it by id, descending, it should appear as C, B, A
        But we expect it to have no effect, so it will stil be A, B, C
        """

        ratings = [3, 2, 1]
        for rating in ratings:
            rating_factory.create(article=article, rating=rating)

        invalid_queries = ["-pkid"]

        endpoint = get_endpoint(article.id)

        for query in invalid_queries:
            query_term = {"ordering": query}

            resp = authenticated_client.get(endpoint, data=query_term)
            assert resp.status_code == status.HTTP_200_OK

            # Assert: request result should not be the same as gthe manual ordered results
            rating = Rating.objects.filter(article=article).order_by(query).first()
            assert resp.data["results"][0]["id"] != str(rating.id)

    # test filter query ==, >=, <=
    def test_valid_filter_query_works_correct(
        self, rating_factory, article, authenticated_client
    ):
        # Arrange: given certain size of varying ratins of an article
        ratings = get_randint_list(5)
        for rating in ratings:
            rating_factory.create(article=article, rating=rating)

        filter_queries = get_filter_queries("rating", ratings)

        # Act
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.get(endpoint, data=filter_queries)

        # Assert
        for query, expected in filter_queries:
            resp = authenticated_client.get(endpoint, data=query)
            assert resp.status_code == status.HTTP_200_OK
            assert resp.data["count"] == expected


class TestRatingCreateEndpoint:
    def test_unauthed_get_401(self, client, article):
        """Test unauthed get 401."""
        data = {"rating": 1, "review": "good"}
        endpoint = get_endpoint(article.id)
        resp = client.post(endpoint, data=data)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authed_get_201_and_data_correct(
        self, authenticated_client, normal_user, article
    ):
        """Test authed get 201 and data correct"""
        data = {"rating": 1, "review": "good"}
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.post(endpoint, data=data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["rating"] == data["rating"]
        assert resp.data["review"] == data["review"]
        assert resp.data["user_full_name"] == normal_user.full_name
        assert resp.data["article_title"] == article.title

    def test_repeating_create_get_400(
        self, authenticated_client, normal_user, article, rating_factory
    ):
        """test repeating create get 400."""
        # Arrange
        rating_factory.create(user=normal_user, article=article)

        # Act
        data = {"rating": 1, "review": "good"}
        endpoint = get_endpoint(article.id)
        resp = authenticated_client.post(endpoint, data=data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert str(resp.data["detail"]) == "You have already rated this article."

    # test rating on non-existing article get 404
    def test_create_with_non_existing_article_get_404(self, authenticated_client):
        endpoint = get_endpoint(uuid4())
        data = {"rating": 1, "review": "good"}
        resp = authenticated_client.post(endpoint, data=data)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # test invalid data type get 400
    def test_create_with_invalid_data_get_400(self, authenticated_client, article):
        endpoint = get_endpoint(article.id)

        invalid_rating = [-1, 6]
        for rating in invalid_rating:
            data = {"rating": rating, "review": "good"}
            resp = authenticated_client.post(endpoint, data=data)
            assert resp.status_code == status.HTTP_400_BAD_REQUEST

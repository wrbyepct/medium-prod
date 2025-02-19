import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Article
from core.apps.bookmarks.serializers import BookmarkSerializer

pytestmark = pytest.mark.django_db


def get_endpoint(slug):
    return reverse("bookmarks_list", args=[slug])


class TestBookmarkListEndpoint:
    def test_unauthed_get_401(self, client, reading_category_factory):
        cate = reading_category_factory.create()
        endpoint = get_endpoint(slug=cate.slug)

        resp = client.get(endpoint)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # auhted get 200 and data correct
    def test_authed_get_200_and_data_correct(
        self,
        reading_category_factory,
        normal_user,
        authenticated_client,
        article_factory,
    ):
        # Arrange: given 3 article in the user's category
        bookmarks_num = 3
        cate = reading_category_factory.create(
            with_bookmarks=bookmarks_num,
            user=normal_user,
        )

        # Arrange: given 2 article not in the category
        not_bookmark_num = 2
        article_factory.create_batch(size=not_bookmark_num)

        # Act
        endpoint = get_endpoint(cate.slug)
        resp = authenticated_client.get(endpoint)

        # Assert response correct
        assert resp.status_code == status.HTTP_200_OK

        bookmarks = cate.bookmarks.all()
        serializer = BookmarkSerializer(bookmarks, many=True)

        # Assert data correct
        assert Article.objects.count() == bookmarks_num + not_bookmark_num
        assert len(resp.data["results"]) == bookmarks_num
        assert resp.data["results"] == serializer.data

    # get not own and data return correctly
    def test_get_not_own_category_bookmarks_200_and_data_correct(
        self,
        reading_category_factory,
        authenticated_client,
        article_factory,
    ):
        # Arrange: given 1 article in the other user's category
        bookmarks_num = 1
        cate = reading_category_factory.create(
            with_bookmarks=bookmarks_num,
            is_private=False,
        )

        # Act
        endpoint = get_endpoint(cate.slug)
        resp = authenticated_client.get(endpoint)

        # Assert response correct
        assert resp.status_code == status.HTTP_200_OK

        bookmarks = cate.bookmarks.all()
        serializer = BookmarkSerializer(bookmarks, many=True)

        # Assert data correct
        assert len(resp.data["results"]) == bookmarks_num
        assert resp.data["results"] == serializer.data

    # not own but private get permission denied 403
    def test_get_other_user_private_cateogry_bookmarks_get_403(
        self, authenticated_client, reading_category_factory
    ):
        cate = reading_category_factory.create(is_private=True)

        endpoint = get_endpoint(slug=cate.slug)

        resp = authenticated_client.get(endpoint)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

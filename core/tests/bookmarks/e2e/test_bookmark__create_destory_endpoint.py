from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def get_endpoint(slug, article_id):
    return reverse("bookmark_create_delete", args=[slug, article_id])


class TestBookmarkCreateEndpoint:
    # unauth get 401
    def test_unauthed_get_401(self, client, article, reading_category_factory):
        cate = reading_category_factory.create()
        endpoint = get_endpoint(slug=cate.slug, article_id=article.id)

        resp = client.post(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # auth get and data correct 201
    def test_authed_get_201_and_bookmark_added(
        self,
        authenticated_client,
        normal_user,
        article,
        reading_category_factory,
    ):
        cate = reading_category_factory.create(user=normal_user)
        endpoint = get_endpoint(slug=cate.slug, article_id=article.id)

        # Act
        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_201_CREATED
        assert article in cate.bookmarks.all()

    def test_add_article_to_not_own_category_get_404(
        self,
        authenticated_client,
        reading_category_factory,
        article,
    ):
        cate = reading_category_factory.create()
        endpoint = get_endpoint(slug=cate.slug, article_id=article.id)

        # Act
        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert article not in cate.bookmarks.all()

    # article not exists raise 404
    def test_article_not_exist_get_404(
        self,
        authenticated_client,
        normal_user,
        reading_category_factory,
    ):
        cate = reading_category_factory(user=normal_user)
        endpoint = get_endpoint(slug=cate.slug, article_id=uuid4())
        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert cate.bookmarks.count() == 0

    # category not exists raise 404
    def test_category_not_found_by_slug_get_404(
        self,
        authenticated_client,
        article,
    ):
        endpoint = get_endpoint(slug="fake", article_id=article.id)
        resp = authenticated_client.post(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestBookmarkDestroyEndpoint:
    # unauth get 401
    def test_unauthed_get_401(self, client, reading_category_factory, article):
        cate = reading_category_factory.create()
        endpoint = get_endpoint(slug=cate.slug, article_id=article.id)

        resp = client.delete(endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    # auth get and data correct 201
    def test_authed_get_200_and_delete_succesfully(
        self,
        authenticated_client,
        normal_user,
        reading_category_factory,
        article,
    ):
        cate = reading_category_factory.create(user=normal_user)
        cate.bookmarks.add(article)
        assert cate.bookmarks.count() == 1
        endpoint = get_endpoint(slug=cate.slug, article_id=article.id)

        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_200_OK
        assert cate.bookmarks.count() == 0

    # article not exists raise 404
    def test_article_not_exist_get_404(
        self,
        reading_category_factory,
        authenticated_client,
        normal_user,
    ):
        cate = reading_category_factory.create(user=normal_user)

        endpoint = get_endpoint(slug=cate.slug, article_id=uuid4())
        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    # category not exists raise 404
    def test_category_not_exist_get_404(self, article, authenticated_client):
        endpoint = get_endpoint(slug="fake", article_id=article.id)

        resp = authenticated_client.delete(endpoint)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

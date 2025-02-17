import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.articles.models import Article
from core.apps.bookmarks.models import ReadingCategory
from core.apps.bookmarks.serializers import BookmarkSerializer

pytestmark = pytest.mark.django_db


@pytest.fixture
def valid_data():
    return {
        "title": "Test Title A",
        "description": "Test description",
        "is_private": True,
    }


@pytest.mark.bbb
class TestBookmarkCategoryCreateEndpoint:
    endpoint = reverse("bookmark_create")

    # unauth get 401 authed get 200
    def test_unauthed_get_401(self, client):
        resp = client.post(self.endpoint)

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_new_category_with_valid_data_but_no_article_id_and_get_201(
        self, valid_data, authenticated_client, normal_user
    ):
        # Act
        resp = authenticated_client.post(self.endpoint, data=valid_data)

        user_cate = ReadingCategory.objects.filter(
            user=normal_user,
            title=valid_data["title"],
            description=valid_data["description"],
        )

        assert user_cate.exists()
        user_cate = user_cate.first()

        assert resp.status_code == status.HTTP_201_CREATED

        assert resp.data["id"] == str(user_cate.id)
        assert resp.data["title"] == valid_data["title"]
        assert resp.data["description"] == valid_data["description"]
        assert resp.data["is_private"] == valid_data["is_private"]
        assert resp.data["slug"] is not None
        assert resp.data["bookmarks"] == []

    def test_create_new_category_with_valid_data_and_article_id_get_201(
        self, valid_data, authenticated_client, normal_user, article
    ):
        article_id = article.id
        resp = authenticated_client.post(
            self.endpoint, data=valid_data, QUERY_STRING=f"article_id={article_id}"
        )

        assert resp.status_code == status.HTTP_201_CREATED

        user_cate = ReadingCategory.objects.get(
            user=normal_user,
            title=valid_data["title"],
            description=valid_data["description"],
        )

        # Assert: Article indeed in user's bookmark category
        article = Article.statistic_objects.preview_data().get(id=article_id)
        assert article in user_cate.bookmarks.all()

        # Assert: Bookmark data serialized correct
        article_serializer = BookmarkSerializer(article)
        assert len(resp.data["bookmarks"]) == 1
        assert resp.data["bookmarks"][0] == article_serializer.data

    @pytest.mark.parametrize("invalid_title", ["", None, "a" * 61])
    def test_create_new_category_with_invalid_title_get_400(
        self, authenticated_client, invalid_title
    ):
        assert ReadingCategory.objects.count() == 0
        invalid_data = {"title": invalid_title, "description": "test"}

        if invalid_title is None:
            invalid_data.pop("title")

        resp = authenticated_client.post(self.endpoint, data=invalid_data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert ReadingCategory.objects.count() == 0

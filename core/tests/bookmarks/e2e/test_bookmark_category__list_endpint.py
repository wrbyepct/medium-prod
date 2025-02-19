import pytest
from django.urls import reverse
from rest_framework import status

from core.apps.bookmarks.models import ReadingCategory
from core.apps.bookmarks.serializers import ReadingCategorySerializer

pytestmark = pytest.mark.django_db


class TestBookmarkCategoryEndpoint:
    endpoint = reverse("bookmark_category_list")

    # unauth get 401 & authed get 200
    def test_unauthed_get_401(self, client, authenticated_client):
        resp = client.get(self.endpoint)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

        resp = authenticated_client.get(self.endpoint)
        assert resp.status_code == status.HTTP_200_OK

    # get data & order correct(return user own only)
    def test_data_correct_with_order(
        self,
        authenticated_client,
        normal_user,
        reading_category_factory,
    ):
        user_own_num = 3
        reading_category_factory.create_batch(
            size=user_own_num,
            user=normal_user,
        )

        non_own_num = 2
        reading_category_factory.create_batch(
            size=non_own_num,
        )

        # Act
        resp = authenticated_client.get(self.endpoint)

        # Assert
        user_own_cates = ReadingCategory.objects.filter(user=normal_user).order_by(
            "-is_reading_list", "-updated_at"
        )
        serializer = ReadingCategorySerializer(user_own_cates, many=True)
        assert len(resp.data) == user_own_num
        assert resp.data == serializer.data

import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_user_create__signal_also_create_category_and_profile():
    user_info = {
        "email": "test@example.com",
        "first_name": "Test_First_Name",
        "last_name": "Test_First_Name",
        "password": "testpassword",
    }
    user = User.objects.create_user(**user_info)
    assert user.profile is not None
    assert user.bookmark_categories.all().count() == 1


def test_admin_create__signal_also_create_category_and_profile():
    user_info = {
        "email": "test@example.com",
        "first_name": "Test_First_Name",
        "last_name": "Test_First_Name",
        "password": "testpassword",
    }
    user = User.objects.create_superuser(**user_info)
    assert user.profile is not None
    assert user.bookmark_categories.all().count() == 1

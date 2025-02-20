import pytest
from django.contrib.auth import get_user_model

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.user(type="signal"),
]

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
    assert user.reading_categories.count() == 1

    cate = user.reading_categories.first()
    assert cate.is_reading_list


def test_admin_create__signal_also_create_category_and_profile():
    user_info = {
        "email": "test@example.com",
        "first_name": "Test_First_Name",
        "last_name": "Test_First_Name",
        "password": "testpassword",
    }
    user = User.objects.create_superuser(**user_info)
    assert user.profile is not None
    assert user.reading_categories.count() == 1

    cate = user.reading_categories.first()
    assert cate.is_reading_list

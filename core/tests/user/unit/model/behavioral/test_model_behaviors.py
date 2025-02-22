# ruff: noqa: PT011
import pytest
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db, pytest.mark.unit, pytest.mark.user(type="model")]

User = get_user_model()


class TestUserCreationSuccessful:
    user_info = {
        "email": "test@example.com",
        "first_name": "Test_First_Name",
        "last_name": "Test_First_Name",
        "password": "testpassword",
    }

    def test_user_model_behavior__create_regular_user_sucessful(self, user_factory):
        # Arrange
        user_info = self.user_info

        # Act
        user = user_factory.create(**user_info)

        # Assert
        assert user.email == user_info["email"]
        assert user.first_name == user_info["first_name"]
        assert user.last_name == user_info["last_name"]
        assert user.check_password(user_info["password"])
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_user_behavior__create_superuser_successful(
        self,
        user_factory,
    ):
        user_info = self.user_info
        user_info["is_staff"] = True
        user_info["is_superuser"] = True

        super_user = user_factory.create(**user_info)

        assert super_user.first_name is not None
        assert super_user.last_name is not None
        assert super_user.email is not None
        assert super_user.password is not None
        assert super_user.is_active
        assert super_user.is_staff
        assert super_user.is_superuser


def test_user_behavior__str_method_sucessful(normal_user):
    assert str(normal_user) == f"{normal_user.first_name} | {normal_user.email}"


def test_user_behavior__get_fullname_successfull(normal_user):
    first_name = normal_user.first_name
    last_name = normal_user.last_name
    assert normal_user.full_name == f"{first_name.title()} {last_name.title()}"


def test_user_behavior__get_short_name_successfull(normal_user):
    first_name = normal_user.first_name

    assert normal_user.short_name == first_name


def test_user_behavior__update_info_sucessful(normal_user):
    new_first_name = "Test_new_first"
    new_last_name = "Test_new_last"
    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.save()

    assert normal_user.first_name == new_first_name
    assert normal_user.last_name == new_last_name


def test_user_behavior__delete_user_successful(normal_user):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_pk)


def test_user_model_behavior__normalize_email_correct(super_user, normal_user):
    email_1 = super_user.email
    email_2 = normal_user.email
    assert email_1 == email_1.lower()
    assert email_2 == email_2.lower()

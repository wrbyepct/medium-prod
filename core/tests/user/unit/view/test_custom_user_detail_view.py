import pytest

from core.apps.user.views import CustomUserDetailsView

pytestmark = [pytest.mark.unit, pytest.mark.user(type="view")]


def test_user_detail_view__get_object_return_requesting_user(mocker):
    request = mocker.Mock(user="stub_user")
    view = CustomUserDetailsView()
    view.request = request

    # Act
    assert view.get_object() == request.user


def test_user_detail_view__get_queryset_return_empty_set():
    view = CustomUserDetailsView()

    # Act
    assert not view.get_queryset()

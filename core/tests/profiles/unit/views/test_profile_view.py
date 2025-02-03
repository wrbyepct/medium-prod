import pytest

from core.apps.profiles.views import (
    BaseFollowListView,
    FollowersListAPIView,
    FollowingListAPIView,
    ProfileUpdateAPIView,
)

pytestmark = pytest.mark.django_db


FOLLOW_QUERY_EXLCLUDE_COLUMN_LIST = [
    "phone_number",
    "gender",
    "country",
    "city",
    "email",
]


def test_profile_base_follow_list_view__get_queryset_correct(profile_factory, mocker):
    profile_factory.create_batch(size=5)

    view = BaseFollowListView()
    qs = view.get_queryset()
    sql = str(qs.query)

    for col in FOLLOW_QUERY_EXLCLUDE_COLUMN_LIST:
        assert col not in sql


def test_profile_followers_list_view__get_queryset_return_user_followers_profiles(
    profile_factory,
):
    p = profile_factory.create(with_followers=3)

    idol = p.user
    view = FollowersListAPIView(user_id=idol.id)
    view.kwargs = {"user_id": idol.id}

    # Act
    qs = view.get_queryset()

    # Assert those profiles indeed have the idol in their following
    for profile in qs:
        assert profile.following.filter(user=idol).exists()


def test_profile_following_list_view__get_queryset_returns_user_following_profiles(
    profile_factory,
):
    p = profile_factory.create(with_following=3)

    user = p.user
    view = FollowingListAPIView()
    view.kwargs = {"user_id": user.id}

    qs = view.get_queryset()

    for profile in qs:
        assert profile.followers.filter(user=user).exists()


def test_profile_update_view__get_object_return_user_profile(
    mocker, normal_user, create_profile
):
    mock_request = mocker.Mock()
    mock_request.user = normal_user

    view = ProfileUpdateAPIView()
    view.request = mock_request

    retrieved_profile = view.get_object()
    assert retrieved_profile == normal_user.profile
    assert view.request.user == normal_user

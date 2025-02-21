from uuid import uuid4

import pytest
from django.http import Http404

from core.apps.profiles.views import (
    BaseFollowListView,
    FollowersListAPIView,
    FollowingListAPIView,
    ProfileUpdateAPIView,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.unit,
    pytest.mark.profile(type="view"),
]


FOLLOW_QUERY_EXLCLUDE_COLUMN_LIST = [
    "phone_number",
    "gender",
    "country",
    "city",
    "email",
]


def test_profile_base_follow_list_view__get_queryset_correct(profile_factory, mocker):
    p = profile_factory.create(with_followers=2)

    view = BaseFollowListView()
    view.kwargs = {"profile_id": p.id}
    view.follow_type = "followers"

    # Act
    qs = view.get_queryset()
    # Assert
    sql = str(qs.query)
    for col in FOLLOW_QUERY_EXLCLUDE_COLUMN_LIST:
        assert col not in sql


def test_profile_base_follow_list_view__get_non_existing_profile_raise_404():
    view = BaseFollowListView()
    view.kwargs = {"profile_id": uuid4()}
    view.follow_type = "followers"

    with pytest.raises(Http404):
        view.get_queryset()


def test_profile_followers_list_view__get_queryset_return_user_followers_profiles(
    profile_factory,
):
    # Arrange: given a profile with 3 followers
    p = profile_factory.create(with_followers=3)

    # Arrange: and a view provided with the profile's id
    user = p.user
    view = FollowersListAPIView()
    view.kwargs = {"profile_id": p.id}

    # Act
    qs = view.get_queryset()

    # Assert those profiles indeed have the idol in their following
    for profile in qs:
        assert profile.following.filter(user=user).exists()


@pytest.mark.sss
def test_profile_following_list_view__get_queryset_returns_user_following_profiles(
    profile_factory,
):
    p = profile_factory.create(with_following=3)
    user = p.user

    view = FollowingListAPIView()
    view.kwargs = {"profile_id": p.id}

    # Act
    qs = view.get_queryset()

    for profile in qs:
        assert profile.followers.filter(user=user).exists()


def test_profile_update_view__get_object_return_user_profile(
    mocker, normal_user, create_profile_for_normal_user
):
    view = ProfileUpdateAPIView()
    view.request = mocker.Mock(user=normal_user)

    # Act
    retrieved_profile = view.get_object()

    assert retrieved_profile == normal_user.profile
    assert view.request.user == normal_user

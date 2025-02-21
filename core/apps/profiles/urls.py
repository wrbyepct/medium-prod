"""Profile view urls."""

from django.urls import path

from .views import (
    FollowAPIView,
    FollowersListAPIView,
    FollowingListAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    UnfollowAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all_profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="me"),
    path("me/update/", ProfileUpdateAPIView.as_view(), name="me_update_profile"),
    path(
        "<uuid:profile_id>/following/",
        FollowingListAPIView.as_view(),
        name="user_following",
    ),
    path(
        "<uuid:profile_id>/followers/",
        FollowersListAPIView.as_view(),
        name="user_followers",
    ),
    path("<uuid:profile_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:profile_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]

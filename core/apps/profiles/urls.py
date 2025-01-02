"""Profile view urls."""

from django.urls import path

from .views import (
    FollowAPIView,
    FollowersListAPIView,
    FollowingAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    UnfollowAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all_profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="me"),
    path("me/update/", ProfileUpdateAPIView.as_view(), name="me_update_profile"),
    path("me/followers/", FollowersListAPIView.as_view(), name="me_followers"),
    path("me/following/", FollowingAPIView.as_view(), name="me_following"),
    path(
        "<uuid:user_id>/followers/", FollowingAPIView.as_view(), name="user_followers"
    ),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnfollowAPIView.as_view(), name="unfollow"),
]

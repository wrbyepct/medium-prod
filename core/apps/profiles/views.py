"""Profile views."""

# ruff: noqa: A002, ANN001, ARG002
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView

from .models import Profile
from .paginations import ProfilePagination
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer
from .services import FollowHandleService

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    """Profile List API View."""

    queryset = Profile.objects.all().join_user_table()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """Profile detail API view."""

    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        Optimize query by joining the user table.

        So you don't have to query through profile for user.
        """
        return Profile.objects.all().join_user_table()

    def get_object(self):
        """Get object filter by requesting user."""
        user = self.request.user
        return self.get_queryset().get(user=user)


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """Profile API view for partial update."""

    serializer_class = UpdateProfileSerializer

    def get_object(self):
        """
        Get profile directly through user's profile field.

        So we don't need to query through profile objects with id like default.
        """
        return self.request.user.profile


class BaseFollowListView(generics.ListAPIView):
    """Template view for Following/Followers list view."""

    serializer_class = FollowingSerializer
    pagination_class = ProfilePagination

    def get_queryset(self):
        """
        Return instances with necessary columns.

        Columns:
           - profile_photo
           - about_me
           - twitter_handle
           - user__first_name
           - user__last_name

        By selecting joined table from user.
        """
        profile_id = self.kwargs.get("profile_id")
        profile = get_object_or_404(Profile, id=profile_id)

        follow_type = self.follow_type
        qs = getattr(profile, follow_type).all()
        return qs.follow_preview_info()


class FollowersListAPIView(BaseFollowListView):
    """Get user's followers by specifying user uuid."""

    follow_type = "followers"


class FollowingListAPIView(BaseFollowListView):
    """Get user's following by specifying user uuid."""

    follow_type = "following"


class FollowAPIView(APIView):
    """Follow API View."""

    def post(self, request, profile_id, format=None, *args, **kwargs):
        """To follow a user."""
        requesting_profile = request.user.profile
        service = FollowHandleService(requesting_profile, profile_id)

        service.check_invalid_follow()

        return service.perform_follow()


class UnfollowAPIView(APIView):
    """View to unfollow a user."""

    def post(self, request, profile_id, *args, **kwargs):
        """To unfollow a user."""
        requesting_profile = request.user.profile
        service = FollowHandleService(requesting_profile, profile_id)

        service.check_invalid_unfollow()
        return service.perform_unfollow()

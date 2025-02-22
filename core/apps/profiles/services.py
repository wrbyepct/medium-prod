"""Profile Follow Service."""
# ruff: noqa: ANN001, ANN204, D107

import logging
from uuid import UUID

from rest_framework import status
from rest_framework.response import Response

from core.apps.profiles.models import Profile
from core.tools.email import inform_followed

from . import exceptions

logger = logging.getLogger(__name__)


class FollowHandleService:
    """
    Profile service to handle follow actions & errors.

    Initialize a follow service with a requesting profile and target profile id.

    Args:
        requesting_profile (Profile): Requester's profile
        target_profile_id (UUID): Action target profile's id

    """

    def __init__(self, requesting_profile: Profile, target_profile_id: UUID):
        self.requesting_profile = requesting_profile
        self.target_profile = self._get_target_profile(target_profile_id)

    def check_invalid_follow(self):
        """
        Raise error if user is trying to do invalid follow actions.

        Invalid actions:
            1. Follow self
            2. Follow the profile they have already been following
        """
        self._handle_follow_self()
        self._handle_repeating_follow()

    def perform_follow(self):
        """
        Pefrom success follow actions.

        Actions:
            1. Add to-follow profile to requesting-profile's following.
            2. Send inform email to to-follow user.
            3. Return success message.
        """
        self.requesting_profile.follow(self.target_profile)
        self._handle_inform_followed()

        to_follow_user = self.target_profile.user

        return Response(
            {
                "message": f"You successfully followed {to_follow_user.full_name}.",
            },
            status=status.HTTP_200_OK,
        )

    def check_invalid_unfollow(self):
        """
        Raise error if user is trying to do invalid unfollow actions.

        Invalid actions:
           - Unfollow a profile they have not yet followed.
        """
        self._handle_unfollow_but_not_yet_followed()

    def perform_unfollow(self):
        """
        Pefrom success unfollow actions.

        Actions:
            1. Remove to-unfollow profile from requesting-profile's following.
            2. Return success message.
        """
        self.requesting_profile.unfollow(self.target_profile)

        to_unfollow_user = self.target_profile.user
        return Response(
            {
                "message": f"You have unfollowed {to_unfollow_user.full_name}.",
            },
            status=status.HTTP_200_OK,
        )

    def _get_target_profile(self, profile_id):
        """
        Return target profile.

        Raise FollowUnfollowTargetNotFound if not found.
        """
        try:
            return Profile.objects.get(id=profile_id)

        except Profile.DoesNotExist as profile_not_found:
            raise exceptions.FollowUnfollowTargetNotFound from profile_not_found

    def _handle_repeating_follow(self):
        """Raise RepeatFollowException if the requesting profile already followed the target."""
        if self.requesting_profile.has_followed(self.target_profile):
            raise exceptions.RepeatFollowException

    def _handle_follow_self(self):
        """Raise CantFollowYourselfException if requesting profile is the same as target profile."""
        to_follow_id = self.target_profile.id
        requesting_id = self.requesting_profile.id

        if requesting_id == to_follow_id:
            raise exceptions.CantFollowYourselfException

    def _handle_inform_followed(self):
        """
        Inform target user being followed.

        Handle error happening during email sending.
        """
        to_follow_user = self.target_profile.user
        request_user = self.requesting_profile.user

        email_data = {
            "being_followed_user_first_name": to_follow_user.first_name,
            "to_email": to_follow_user.email,
            "user_fullname": request_user.full_name,
        }

        try:
            inform_followed(**email_data)
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Error happens during inform user being followed: {e}")

    def _handle_unfollow_but_not_yet_followed(self):
        """Rasie UnfollowButNotYetFollowException if target profile has not been followed yet."""
        if not self.requesting_profile.has_followed(self.target_profile):
            raise exceptions.UnfollowButNotYetFollowException

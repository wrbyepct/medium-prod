"""Custom exception."""

from rest_framework.exceptions import APIException


class CantFollowYourselfException(APIException):
    """Cannot self-follow expection."""

    status_code = 403
    default_detail = "You cannot follow yourself."
    default_code = "forbidden"


class RepeatFollowException(APIException):
    """Cannot repeat follow exception."""

    status_code = 400
    default_detail = "You already followed that user."


class UnfollowButNotYetFollowException(APIException):
    """Cannot repeat follow exception."""

    status_code = 400
    default_detail = "Oops, you can't unfollow a user that you haven't follwoed!"


class FollowUnfollowTargetNotFound(APIException):
    """Cannot find follow/unfollow target."""

    status_code = 404
    default_detail = " You can't follow/unfollow a profile that does not exist."

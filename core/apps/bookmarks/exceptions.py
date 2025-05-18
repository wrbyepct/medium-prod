"""Bookmark exceptions."""

from rest_framework.exceptions import APIException


class YouCannotBookmarkAgain(APIException):
    """Custom API exception, you cannot bookmark the same article."""

    status_code = 400
    default_code = "bad_request"
    default_detail = "You already bookmarked the same article."


class SignalProcessingError(Exception):
    """Handle error happening in signal."""


class TitleEmptyError(APIException):
    """Custom API exception, title field must be filed if no existing category specified."""

    status_code = 400
    default_code = "bad_request"
    default_detail = "title field must if reuiqred if no existing category specified."


class TitleTooLongError(APIException):
    """Custom API exception, title length must be within 60."""

    status_code = 400
    default_code = "bad_request"
    default_detail = "title length must be within 60"

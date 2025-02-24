"""Custom APIException for Response views."""

from rest_framework.exceptions import APIException


class CannotRepeatClap(APIException):
    """Cannot Repeat clapping the same response of an article."""

    status_code = 400
    default_detail = "You have already clapped this response."

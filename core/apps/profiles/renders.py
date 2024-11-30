"""Renderer classes."""

# ruff: noqa: ANN001, ARG002
import json

from rest_framework.renderers import JSONRenderer


class ProfileRenderer(JSONRenderer):
    """Custom Renderer class to render single profile."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, rederer_context=None):
        """
        Render Profile data.

        Detail:
        -------
        Render response using 'profile' as key.

        If error, use default super method.
        """
        error = data.get("error", None)
        if error is not None:
            return super().render(data)

        status_code = rederer_context["response"].status_code

        return json.dumps({"status_code": status_code, "profile": data})


class ProfileListRenderer(JSONRenderer):
    """Custom Renderer class to render a list of profile."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, rederer_context=None):
        """
        Render Profile data.

        Detail:
        -------
        Render response using 'profile_list' as key.

        If error, use default super method.
        """
        error = data.get("error", None)
        if error is not None:
            return super().render(data)

        status_code = rederer_context["response"].status_code

        return json.dumps({"status_code": status_code, "profile_list": data})

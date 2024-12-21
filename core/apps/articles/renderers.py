"""Articles renderers."""

import json
import logging

from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)


class ArticleRenderer(JSONRenderer):
    """Custom Article render class."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the data with this format.

        {
            "status_code": <status code>,
            "article": <article data>
        }
        """
        # If article is empty we return 200 ok
        status_code = (
            renderer_context["response"].status_code
            if renderer_context is not None
            else 200
        )
        # If article is empty we return no error
        errors = data.get("errors", None)

        if errors is not None:
            return super().render(data)

        return json.dumps({"status_code": status_code, "article": data}, indent=4)


class ArticleListRenderer(JSONRenderer):
    """Custom Article List Renderer."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the data with this format for all clients, including the browsable API.

        {
            "status_code": <status code>,
            "article_list": <article_list data>
        }
        """
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        # Custom error handling (if present)
        if errors is not None:
            return super().render(data)

        # Wrap response in desired format
        wrapped_data = {
            "status_code": status_code,
            "article_list": data,
        }
        if accepted_media_type == "text/html":
            return wrapped_data
        return json.dumps(wrapped_data, indent=4)

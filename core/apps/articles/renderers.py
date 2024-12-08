"""Articles renderers."""

import json

from rest_framework.renderers import JSONRenderer


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
            if renderer_context is None
            else 201
        )
        # If article is empty we return no error
        errors = data.get("errors", None) if data is not None else None

        if errors is not None:
            return super().render(data)

        return json.dumps({"status_code": status_code, "article": data})


class ArticleListRenderer(JSONRenderer):
    """Custom Article List Renderer."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the data with this format.

        {
            "status_code": <status code>,
            "article_list": <article_list data>
        }
        """
        errors = data.get("errors", None)
        status_code = renderer_context["response"].status_code

        if errors is not None:
            return super().render(data)

        return json.dumps({"status_code": status_code, "article_list": data})

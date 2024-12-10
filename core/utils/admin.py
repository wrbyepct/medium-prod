"""Utils for admin page."""

from django.urls import reverse
from django.utils.html import format_html


def get_model_change_page(app_name: str, model_name: str, obj_id: int):
    """
    Return the instance admin change page link, if not found return 'N/A'.

    Args:
        app_name (str): the app's name.
        model_name (str): the model's name.
        obj_id (int): the retrieving instance's id.

    Returns:
        SafeText or "N/A"

    """
    if obj_id:
        url = reverse(f"admin:{app_name}_{model_name}_change", args=[obj_id])
        return format_html("<a href={}>Click me</a>", url)
    return "N/A"

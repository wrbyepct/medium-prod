"""Utilities for hash."""

# ruff: noqa: ANN001
import hashlib

from django.utils.text import slugify


def generate_hashed_slug(instance):
    """Slugify an model instance."""
    base_slug = slugify(instance.title)
    if instance.slug is not None:
        hash_part = instance.slug.split("-")[-1]
    else:
        hash_part = hashlib.md5(str(instance.id).encode("utf-8")).hexdigest()[:13]  # noqa: S324
    return f"{base_slug}-{hash_part}"

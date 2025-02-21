"""Util file handling functions."""

# ruff: noqa: ANN001, ARG001
from pathlib import Path
from uuid import uuid4


def generate_file_path(instance, filename: str, app_name: str):
    """
    Change uploaded image file name to uuid4 string + extension.

    For example: uploads/<app_name>/<uuid4>.jpg
    """
    path = Path(filename)
    ext = path.suffix
    hash_name = f"{uuid4()}{ext}"
    return Path("uploads") / app_name / hash_name

from __future__ import annotations

import os  # noqa: F401
from pathlib import Path

import environ
from split_settings.tools import include, optional

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = ROOT_DIR / "apps"
DEBUG = env.bool("DJANGO_DEBUG", False)
IN_DOCKER = env.bool("IN_DOCKER", False)


STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

project_settings = "production.py"

local_dev_preference: str | Path = ""

if DEBUG:
    project_settings = "local.py"
    local_dev_preference = ROOT_DIR / "local/settings.dev.py"

if IN_DOCKER:
    STATIC_ROOT = "/vol/api/staticfiles/"
    MEDIA_ROOT = "/vol/api/mediafiles/"


include(
    "base.py",
    "project.py",
    "loggings.py",
    project_settings,
    optional(str(local_dev_preference)),
)

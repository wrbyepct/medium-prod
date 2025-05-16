# ruff: noqa: T201, ERA001
from __future__ import annotations

from pathlib import Path

import environ
from split_settings.tools import include

env = environ.Env()

"""
Default settings
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = ROOT_DIR / "apps"
DEBUG = env.bool("DJANGO_DEBUG", default=False)

IN_DOCKER = env.bool("IN_DOCKER", default=False)
IN_TEST = env.bool("IN_TEST", default=False)
IN_GITHUB = env.bool("IN_GITHUB", default=False)

STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

project_settings = "production.py"


settings = [
    "base.py",
    "project.py",
]


"""
Dynamically change settings
"""

if DEBUG:
    project_settings = "local.py"
    settings += [
        "loggings.py",
    ]

if IN_DOCKER:
    STATIC_ROOT = "/vol/api/staticfiles/"
    MEDIA_ROOT = "/vol/api/mediafiles/"

if IN_GITHUB:
    project_settings = "github.py"


settings += [project_settings]

include(*settings)

from pathlib import Path

import environ
from split_settings.tools import include

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = ROOT_DIR / "apps"
DEBUG = env.bool("DJANGO_DEBUG", False)


STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

project_settings = "local.py" if DEBUG else "production.py"

include(
    "base.py",
    project_settings,
)

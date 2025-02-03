import pytest
from pytest_factoryboy import register

from .factories import ProfileFactory

register(ProfileFactory)


@pytest.fixture
def profile(profile_factory, mock_media_dir):
    return profile_factory.create()


@pytest.fixture
def two_profiles(profile_factory, mock_media_dir):
    return profile_factory.create_batch(size=2)

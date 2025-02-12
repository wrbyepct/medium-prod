import pytest
from pytest_factoryboy import register

from .factories import RatingFactory

register(RatingFactory)


@pytest.fixture
def rating(rating_factory, normal_user):
    return rating_factory.create(user=normal_user)

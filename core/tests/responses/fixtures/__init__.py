import pytest
from pytest_factoryboy import register

from .factories import ResponseClapFactory, ResponseFactory

register(ResponseFactory)
register(ResponseClapFactory)


@pytest.fixture
def response(response_factory):
    return response_factory.create()

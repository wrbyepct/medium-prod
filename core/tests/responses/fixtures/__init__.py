from pytest_factoryboy import register

from .factories import ResponseClapFactory, ResponseFactory

register(ResponseFactory)
register(ResponseClapFactory)

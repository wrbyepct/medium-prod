from pytest_factoryboy import register

from .factories import BookmarkInCategoryFactory, ReadingCategoryFactory

register(ReadingCategoryFactory)
register(BookmarkInCategoryFactory)

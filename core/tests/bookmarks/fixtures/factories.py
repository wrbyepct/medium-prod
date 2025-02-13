import factory
from faker import Faker

from core.apps.bookmarks.models import BookmarksInCategories, ReadingCategory
from core.tests.articles.fixtures.factories import ArticleFactory
from core.tests.user.fixtures.factories import UserFactory

fake = Faker()


class ReadingCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReadingCategory

    title = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=60))
    description = factory.Faker("sentence", nb_words=5)
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def with_bookmarks(self, create, extracted, *arg, **kwargs):
        if not create:
            return
        if extracted:
            bookmarks = ArticleFactory.create_batch(size=extracted)
            self.bookmarks.set(bookmarks)


class BookmarkInCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookmarksInCategories

    category = factory.SubFactory(ReadingCategoryFactory)
    bookmark = factory.SubFactory(ArticleFactory)

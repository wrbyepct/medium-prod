import factory
from factory import fuzzy

from core.apps.ratings.models import Rating
from core.tests.articles.fixtures.factories import ArticleFactory
from core.tests.user.fixtures.factories import UserFactory


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    review = factory.Faker("sentence", nb_words=5)
    rating = fuzzy.FuzzyChoice([c[0] for c in Rating.RATING_CHOICES])
    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)

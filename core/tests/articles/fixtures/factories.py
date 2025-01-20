import factory
from django.db.models.signals import post_delete, post_save
from faker import Faker

from core.apps.articles.models import Article, ArticleView, Clap
from core.tests.user.fixtures.factories import UserFactory

faker = Faker()


@factory.django.mute_signals(post_save, post_delete)
class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=255))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=255))
    body = factory.Faker("sentence", nb_words=30)

    author = factory.SubFactory(UserFactory)

    class Params:
        with_image = factory.Trait(
            banner_image=factory.django.ImageField(filename="default.jpg")
        )

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.set(extracted)


@factory.django.mute_signals(post_save, post_delete)
class ArticleViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleView

    article = factory.SubFactory(ArticleFactory)

    class Params:
        has_user = factory.Trait(user=factory.SubFactory(UserFactory))
        has_viewer_ip = factory.Trait(viewer_ip=factory.Faker("ipv4"))


@factory.django.mute_signals(post_save, post_delete)
class ArticleClapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clap

    article = factory.SubFactory(ArticleFactory)
    user = factory.SubFactory(UserFactory)

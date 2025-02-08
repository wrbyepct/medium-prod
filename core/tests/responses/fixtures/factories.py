import factory

from core.apps.responses.models import Response, ResponseClap
from core.tests.articles.fixtures.factories import ArticleFactory
from core.tests.user.fixtures.factories import UserFactory


class ResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Response

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)

    class Params:
        with_parent = factory.Trait(
            parent=factory.SubFactory(
                "core.tests.responses.fixtures.factories.ResponseFactory"
            )
        )

    @factory.post_generation
    def with_children(self, create, extracted, *args, **kwargs):
        if not create:
            return
        if extracted:
            responses = ResponseFactory.create_batch(size=extracted)
            self.children.set(responses)

    @factory.post_generation
    def with_claps(self, create, extracted, *args, **kwargs):
        if not create:
            return
        if extracted:
            claps = ResponseClapFactory.create_batch(size=extracted, response=self)
            self.claps.set(claps)


class ResponseClapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResponseClap

    user = factory.SubFactory(UserFactory)
    response = factory.SubFactory(ResponseFactory)

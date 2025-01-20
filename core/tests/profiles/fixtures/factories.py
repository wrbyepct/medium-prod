import factory

from core.apps.profiles.models import Profile
from core.tests.user.fixtures.factories import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    class Params:
        has_followers = factory.Trait(
            followers=factory.RelatedFactoryList(
                "core.tests.profiles.fixtures.factories.ProfileFactory", size=3
            )
        )
        has_following = factory.Trait(
            following=factory.RelatedFactoryList(
                "core.tests.profiles.fixtures.factories.ProfileFactory", size=3
            )
        )

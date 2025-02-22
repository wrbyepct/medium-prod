import factory

from core.apps.profiles.models import Profile
from core.tests.user.fixtures.factories import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def with_followers(self, create, extracted, **kwargs):
        if not extracted:
            return

        if create:
            profiles = ProfileFactory.create_batch(size=extracted)
        else:
            profiles = ProfileFactory.build_batch(size=extracted)

        for p in profiles:
            self.followers.add(p)

    @factory.post_generation
    def with_following(self, create, extracted, **kwargs):
        if not extracted:
            return

        if create:
            profiles = ProfileFactory.create_batch(size=extracted)
        else:
            profiles = ProfileFactory.build_batch(size=extracted)

        for p in profiles:
            self.following.add(p)

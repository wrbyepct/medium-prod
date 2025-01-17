import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from pytest_factoryboy import register

User = get_user_model()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> None:
        """Override create to simulate"""
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        return manager.create_user(*args, **kwargs)


register(UserFactory)

import pytest
from django.db import IntegrityError
from faker import Faker

pytestmark = pytest.mark.django_db

fake = Faker()


def test_article_view_model__violate_unique_constraints(
    article, normal_user, ipv4, article_view_factory, article_factory, user_factory
):
    article_view_factory.create(article=article, user=normal_user, viewer_ip=ipv4)

    # Different article passes
    article_view_factory.create(
        article=article_factory(), user=normal_user, viewer_ip=ipv4
    )

    # Different user passes
    article_view_factory.create(article=article, user=user_factory(), viewer_ip=ipv4)

    # Different ip passes
    article_view_factory.create(
        article=article, user=normal_user, viewer_ip=fake.ipv4()
    )

    # All same violates the unique constraints
    with pytest.raises(IntegrityError):
        article_view_factory.create(article=article, user=normal_user, viewer_ip=ipv4)

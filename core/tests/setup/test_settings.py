import pytest


@pytest.mark.debug
def test_envs():
    from django.conf import settings

    is_debug = settings.DEBUG
    assert not is_debug
    assert settings.IN_TEST

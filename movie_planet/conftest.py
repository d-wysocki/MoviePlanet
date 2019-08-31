import pytest
from django.test import RequestFactory

from movie_planet.movies.factories import MovieFactory


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def movie_factory():
    return MovieFactory()

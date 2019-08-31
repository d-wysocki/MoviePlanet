from movie_planet.movies.clients import OMDbClient
from django.conf import settings
from mock import patch


class TestOMDbClient:
    def test__init__(self):
        client = OMDbClient()

        assert client.apikey == settings.OMDB_API_KEY
        assert client.url == settings.OMDB_URL

    @patch('movie_planet.movies.clients.requests')
    def test_get_movie_by_title(self,mock_requests):
        client = OMDbClient()
        title = 'fancy title'

        client.get_movie_by_title(title)

        mock_requests.get.assert_called_once_with(
            params={'t': title, 'apikey': settings.OMDB_API_KEY},
            url=settings.OMDB_URL
        )

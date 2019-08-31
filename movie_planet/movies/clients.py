import requests
from django.conf import settings


class OMDbClient:
    def __init__(self):
        self.apikey = settings.OMDB_API_KEY
        self.url = settings.OMDB_URL

    def get_movie_by_title(self, title):
        query_params = {"t": title, "apikey": self.apikey}
        response = requests.get(url=self.url, params=query_params)
        return response.json()

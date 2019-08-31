import pytest
from rest_framework.exceptions import ErrorDetail

from movie_planet.movies.api.serializers import (
    CommentSerializer,
    MovieSerializer,
    TopMovieSerializer,
)

pytestmark = pytest.mark.django_db


class TestMovieSerializer:
    def test_to_internal_value(self):
        serializer = MovieSerializer()
        data = {
            "imdbRating": "1",
            "imdbVotes": "1",
            "imdbID": "1",
            "BoxOffice": "1",
            "imdbRating": "1",
            "Title": "fancy title",
            "Released": "N/A",
        }

        result = serializer.to_internal_value(data)

        assert result["imdb_rating"] == "1"
        assert result["imdb_votes"] == "1"
        assert result["imdb_id"] == "1"
        assert result["box_office"] == "1"
        assert result["title"] == "fancy title"
        assert "released" not in result

    def test_valid(self):
        data = {"Title": "fancy title", "Year": "1994"}
        serializer = MovieSerializer(data=data)
        serializer.is_valid()

        result = serializer.data

        assert result["title"] == "fancy title"
        assert result["year"] == "1994"

    def test_invalid(self):
        data = {"Year": "1994-03-11"}
        serializer = MovieSerializer(data=data)

        serializer.is_valid()

        assert serializer.errors == {
            "year": [
                ErrorDetail(
                    string="Date has wrong format. Use one of these formats instead: YYYY.",
                    code="invalid",
                )
            ],
            "title": [ErrorDetail(string="This field is required.", code="required")],
        }


class TestCommentSerializer:
    def test_valid(self, movie_factory):
        data = {"movie": movie_factory.id, "body": "test comment"}
        serializer = CommentSerializer(data=data)
        serializer.is_valid()

        result = serializer.data

        assert result["movie"] == movie_factory.id
        assert result["movie"] == movie_factory.id

    def test_invalid(self, movie_factory):
        data = {"movie": movie_factory.id}
        serializer = CommentSerializer(data=data)

        serializer.is_valid()

        assert serializer.errors == {
            "body": [ErrorDetail(string="This field is required.", code="required")]
        }

        data = {"movie": 999, "body": "test comment"}
        serializer = CommentSerializer(data=data)

        serializer.is_valid()

        assert serializer.errors == {
            "movie": [
                ErrorDetail(
                    string='Invalid pk "999" - object does not exist.',
                    code="does_not_exist",
                )
            ]
        }


class TestTopMovieSerializer:
    def test_valid(self):
        data = {"movie_id": 1, "total_comments": 10, "rank": 100}
        serializer = TopMovieSerializer(data=data)
        serializer.is_valid()

        result = serializer.data

        assert result["movie_id"] == 1
        assert result["total_comments"] == 10
        assert result["rank"] == 100

import pytest
from mock import patch
from movie_planet.movies.api.views import MoviesViewSet, CommentsViewSet, TopViewSet
from rest_framework.exceptions import ErrorDetail
from movie_planet.movies.factories import (
    CommentFactory,
    MovieFactory,
    create_movies_with_rank,
)
from movie_planet.movies.api.serializers import CommentSerializer, TopMovieSerializer
from datetime import datetime, timedelta
from movie_planet.movies.utils import prepare_date_range

pytestmark = pytest.mark.django_db


class TestMoviesViewSet:
    @patch("movie_planet.movies.clients.OMDbClient.get_movie_by_title")
    def test_create(self, mock_get_movie_by_title, request_factory):
        title = "Fancy Title"
        mock_get_movie_by_title.return_value = {"Response": "True", "Title": title}
        view = MoviesViewSet
        request = request_factory.post("/fake-url/", data={"title": title})
        view = view.as_view({"post": "create"})

        result = view(request)

        mock_get_movie_by_title.assert_called_once_with(title)
        assert result.data["title"] == title

        mock_get_movie_by_title.reset_mock()

        result = view(request)

        assert result.data["title"] == title
        assert not mock_get_movie_by_title.called

    @patch("movie_planet.movies.clients.OMDbClient.get_movie_by_title")
    def test_create_without_title(self, mock_get_movie_by_title, request_factory):
        mock_get_movie_by_title.return_value = {"Response": "True"}
        view = MoviesViewSet
        request = request_factory.post("/fake-url/")
        view = view.as_view({"post": "create"})

        result = view(request)

        assert result.status_code == 400
        assert result.data == {"error": "`title` is required"}

    @patch("movie_planet.movies.clients.OMDbClient.get_movie_by_title")
    def test_create_with_404_response(self, mock_get_movie_by_title, request_factory):
        title = "Fancy Title"
        error_response = {"Response": "False", "error": "error"}
        mock_get_movie_by_title.return_value = error_response
        view = MoviesViewSet
        request = request_factory.post("/fake-url/", data={"title": title})
        view = view.as_view({"post": "create"})

        result = view(request)

        mock_get_movie_by_title.assert_called_once_with(title)
        assert result.data == error_response


class TestCommentsViewSet:
    def test_create(self, request_factory, movie_factory):
        comment_data = {"movie": movie_factory.id, "body": "test comment"}
        request = request_factory.post("/fake-url/", data=comment_data)
        view = CommentsViewSet.as_view({"post": "create"})

        result = view(request)

        assert result.status_code == 201
        assert result.data["movie"] == comment_data["movie"]
        assert result.data["body"] == comment_data["body"]

    def test_create_invalid(self, request_factory):
        view = CommentsViewSet.as_view({"post": "create"})
        request = request_factory.post(
            "/fake-url/", data={"movie": 999, "body": "test comment"}
        )

        result = view(request)

        assert result.status_code == 400
        assert result.data == {
            "movie": [
                ErrorDetail(
                    string='Invalid pk "999" - object does not exist.',
                    code="does_not_exist",
                )
            ]
        }

        request = request_factory.post("/fake-url/", data={})

        result = view(request)

        assert result.status_code == 400
        assert result.data == {
            "body": [ErrorDetail(string="This field is required.", code="required")],
            "movie": [ErrorDetail(string="This field is required.", code="required")],
        }

    def test_list(self, request_factory):
        comment_1 = CommentFactory()
        comment_2 = CommentFactory()
        view = CommentsViewSet.as_view({"get": "list"})
        request = request_factory.get("/fake-url/")

        result = view(request)

        assert len(result.data) == 2
        assert result.status_code == 200
        assert result.data == CommentSerializer([comment_1, comment_2], many=True).data

    def test_list_with_filters(self, request_factory):
        comment_1 = CommentFactory()
        comment_2 = CommentFactory()
        movie = MovieFactory()
        comment_3 = CommentFactory(movie=movie)
        view = CommentsViewSet.as_view({"get": "list"})
        request = request_factory.get("/fake-url/")

        result = view(request)

        assert len(result.data) == 3
        assert result.status_code == 200
        assert (
            result.data
            == CommentSerializer([comment_1, comment_2, comment_3], many=True).data
        )

        request = request_factory.get("/fake-url/", {"movie": movie.id})

        result = view(request)

        assert len(result.data) == 1
        assert result.status_code == 200
        assert result.data == CommentSerializer([comment_3], many=True).data


class TestTopViewSet:
    def test_list(self, request_factory):
        from_date = to_date = datetime.today().date()
        movie_1, movie_2, movie_3 = create_movies_with_rank()
        expected_data = [
            {"movie_id": movie_2.id, "total_comments": 2, "rank": 1},
            {"movie_id": movie_3.id, "total_comments": 2, "rank": 1},
            {"movie_id": movie_1.id, "total_comments": 1, "rank": 2},
        ]
        view = TopViewSet.as_view({"get": "list"})
        request = request_factory.get(
            "/fake-url/", {"from_date": from_date, "to_date": to_date}
        )

        result = view(request)

        assert result.status_code == 200
        assert result.data == TopMovieSerializer(expected_data, many=True).data

        request = request_factory.get("/fake-url/", {})

        result = view(request)
        assert result.status_code == 400
        assert result.data == {"error": "`from_date` and `to_date` are required"}

    def test_get_queryset(self):
        from_date = to_date = datetime.today().date()
        created_at = datetime.today() - timedelta(days=5)
        movie_1 = MovieFactory()
        movie_2 = MovieFactory()
        CommentFactory(movie=movie_1)
        comment_2 = CommentFactory(movie=movie_2, created_at=created_at)
        comment_2.created_at = created_at
        comment_2.save()

        view = TopViewSet()
        result = view.get_queryset(prepare_date_range(str(from_date), str(to_date)))

        assert movie_1.id in result
        assert movie_2.id not in result

        view = TopViewSet()
        created_at_date = str(created_at.date())

        result = view.get_queryset(
            prepare_date_range(created_at_date, str(to_date))
        )

        assert movie_1.id in result
        assert movie_2.id in result

        view = TopViewSet()

        result = view.get_queryset(
            prepare_date_range(created_at_date, created_at_date)
        )

        assert movie_1.id not in result
        assert movie_2.id in result

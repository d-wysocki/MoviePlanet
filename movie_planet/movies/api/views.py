from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from movie_planet.movies.api.serializers import (
    CommentSerializer,
    MovieSerializer,
    TopMovieSerializer,
)
from movie_planet.movies.clients import OMDbClient
from movie_planet.movies.models import Comment, Movie
from movie_planet.movies.utils import generate_movie_rank, prepare_date_range


class MoviesViewSet(ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        client = OMDbClient()
        title = request.data.get("title")

        if not title:
            return Response({"error": "`title` is required"}, status=400)
        try:
            data = Movie.objects.get(title=title)
            serializer = MovieSerializer(data)
        except Movie.DoesNotExist:
            data = client.get_movie_by_title(title)
            if eval(data["Response"]) is False:
                return Response(data, status=404)
            serializer = MovieSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)


class CommentsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ("movie",)


class TopViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        if not from_date and not to_date:
            return Response(
                {"error": "`from_date` and `to_date` are required"}, status=400
            )
        queryset = self.get_queryset(prepare_date_range(from_date, to_date))
        serializer = TopMovieSerializer(generate_movie_rank(queryset), many=True)
        return Response(serializer.data)

    def get_queryset(self, date_range):
        return (
            Movie.objects.prefetch_related("comments")
            .filter(comments__created_at__range=date_range)
            .values_list("id", flat=True)
        )

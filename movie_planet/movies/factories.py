from factory import DjangoModelFactory, Sequence, SubFactory

from movie_planet.movies.models import Movie, Comment


class MovieFactory(DjangoModelFactory):
    title = Sequence(lambda n: "Title %03d" % n)

    class Meta:
        model = Movie


class CommentFactory(DjangoModelFactory):
    body = "test body"
    movie = SubFactory(MovieFactory)

    class Meta:
        model = Comment


def create_movies_with_rank():
    movie_1 = MovieFactory()
    movie_2 = MovieFactory()
    movie_3 = MovieFactory()

    CommentFactory(movie=movie_1)
    CommentFactory(movie=movie_2)
    CommentFactory(movie=movie_2)
    CommentFactory(movie=movie_3)
    CommentFactory(movie=movie_3)

    return movie_1, movie_2, movie_3

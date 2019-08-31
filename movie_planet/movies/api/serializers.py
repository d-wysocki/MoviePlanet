from rest_framework import serializers

from movie_planet.movies.models import Comment, Movie

MODEL_FIELDS = {
    "imdbRating": "imdb_rating",
    "imdbVotes": "imdb_votes",
    "imdbID": "imdb_id",
    "BoxOffice": "box_office",
}


class MovieSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        mapped_fields = {
            value: data[key]
            for key, value in MODEL_FIELDS.items()
            if data.get(key) is not None
        }
        data = {
            key.lower(): value
            for key, value in data.items()
            if value != "N/A" or key in MODEL_FIELDS.keys()
        }
        data.update(mapped_fields)

        imdb_rating = data["imdb_rating"]
        if imdb_rating:
            data["imdb_rating"] = self.cast_to_number(imdb_rating, float)

        return super(MovieSerializer, self).to_internal_value(data)

    @staticmethod
    def cast_to_number(string, number_type):
        try:
            return number_type(string)
        except ValueError:
            return None

    class Meta:
        model = Movie
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class TopMovieSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()

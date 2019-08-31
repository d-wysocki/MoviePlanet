from django.contrib.postgres.fields import JSONField
from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Movie(CreatedAtMixin, models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    year = models.CharField(null=True, blank=True, max_length=15)
    rated = models.CharField(null=True, blank=True, max_length=255)
    released = models.CharField(null=True, blank=True, max_length=64)
    runtime = models.CharField(null=True, blank=True, max_length=64)
    genre = models.CharField(null=True, blank=True, max_length=64)
    director = models.CharField(null=True, blank=True, max_length=64)
    writer = models.CharField(null=True, blank=True, max_length=64)
    actors = models.CharField(null=True, blank=True, max_length=255)
    plot = models.CharField(null=True, blank=True, max_length=255)
    language = models.CharField(null=True, blank=True, max_length=64)
    country = models.CharField(null=True, blank=True, max_length=64)
    awards = models.CharField(null=True, blank=True, max_length=255)
    poster = models.CharField(null=True, blank=True, max_length=255)
    ratings = JSONField(null=True, blank=True)
    metascore = models.CharField(null=True, blank=True, max_length=255)
    imdb_rating = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=10
    )
    imdb_votes = models.CharField(null=True, blank=True, max_length=64)
    imdb_id = models.CharField(null=True, blank=True, max_length=64)
    type = models.CharField(null=True, blank=True, max_length=64)
    dvd = models.CharField(null=True, blank=True, max_length=64)
    box_office = models.CharField(null=True, blank=True, max_length=64)
    production = models.CharField(null=True, blank=True, max_length=64)
    website = models.CharField(null=True, blank=True, max_length=64)


class Comment(CreatedAtMixin, models.Model):
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(null=False, blank=False, max_length=255)

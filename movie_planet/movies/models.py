from django.db import models
from django.contrib.postgres.fields import JSONField


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Movie(CreatedAtMixin, models.Model):
    title = models.CharField(blank=False,null=False,max_length=255)
    year = models.DateField(null=True, blank=True)
    rated = models.CharField(null=True, blank=True, max_length=255)
    released = models.CharField(null=True, blank=True, max_length=255)
    runtime = models.CharField(null=True, blank=True, max_length=255)
    genre = models.CharField(null=True, blank=True, max_length=255)
    director = models.CharField(null=True, blank=True, max_length=255)
    writer = models.CharField(null=True, blank=True, max_length=255)
    actors = models.CharField(null=True, blank=True, max_length=255)
    plot = models.CharField(null=True, blank=True, max_length=255)
    language = models.CharField(null=True, blank=True, max_length=255)
    country = models.CharField(null=True, blank=True, max_length=255)
    awards = models.CharField(null=True, blank=True, max_length=255)
    poster = models.CharField(null=True, blank=True, max_length=255)
    ratings = JSONField(null=True, blank=True)
    metascore = models.CharField(null=True, blank=True, max_length=255)
    imdb_rating = models.CharField(null=True, blank=True, max_length=255)
    imdb_votes = models.CharField(null=True, blank=True, max_length=255)
    imdb_id = models.CharField(null=True, blank=True, max_length=255)
    type = models.CharField(null=True, blank=True, max_length=255)
    dvd = models.CharField(null=True, blank=True, max_length=255)
    box_office = models.CharField(null=True, blank=True, max_length=255)
    production = models.CharField(null=True, blank=True, max_length=255)
    website = models.CharField(null=True, blank=True, max_length=255)


class Comment(CreatedAtMixin, models.Model):
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(null=False, blank=False, max_length=255)

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("api/", include("movie_planet.movies.api.urls", namespace="movies")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


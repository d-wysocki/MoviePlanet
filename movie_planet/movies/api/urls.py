from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movie_planet.movies.api import views
app_name = 'movies'
router = DefaultRouter()
router.register(r'movies', views.MoviesViewSet, base_name='movies')
router.register(r'comments', views.CommentsViewSet, base_name='comments')
router.register(r'top', views.TopViewSet, base_name='comments')

urlpatterns = [
    path('', include(router.urls)),
]

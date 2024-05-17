from django.urls import path

from podcast.views import play_podcast

app_name = 'podcast'

urlpatterns = [
    path('<str:podcast_id>/', play_podcast, name='podcast_detail'),
]

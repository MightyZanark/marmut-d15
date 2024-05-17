from django.urls import path

from podcast.views import play_podcast, create_podcast, create_episode, list_podcast, \
                            list_episodes, delete_podcast, delete_episode

app_name = 'podcast'

urlpatterns = [
    path('list/', list_podcast, name='list_podcast'),
    path('create/', create_podcast, name='create_podcast'),
    path('<str:podcast_id>/', play_podcast, name='podcast_detail'),
    path('<str:podcast_id>/delete/', delete_podcast, name='delete_podcast'),
    path('<str:podcast_id>/list-episode/', list_episodes, name='list_episode'),
    path('<str:podcast_id>/create-episode/', create_episode, name='create_episode'),
    path('<str:podcast_id>/delete-episode/<str:episode_id>/', delete_episode, name='delete_episode'),
]

from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('list/', list_album, name = 'list_album'),
    path('create-album/', create_album, name = 'create_album'), 
    path('<str:album_id>/', detail_album, name = 'detail_album'),
    path('<str:album_id>/delete/', delete_album, name = 'delete_album'),
    path('<str:album_id>/create-song/', create_song, name='create_song'),
    path('<str:album_id>/<str:song_id>/', delete_song, name='delete_song')
]


# urlpatterns = [
#     path('list/', list_podcast, name='list_podcast'),
#     path('create/', create_podcast, name='create_podcast'),
#     path('<str:podcast_id>/', play_podcast, name='podcast_detail'),
#     path('<str:podcast_id>/delete/', delete_podcast, name='delete_podcast'),
#     path('<str:podcast_id>/list-episode/', list_episodes, name='list_episode'),
#     path('<str:podcast_id>/create-episode/', create_episode, name='create_episode'),
#     path('<str:podcast_id>/delete-episode/<str:episode_id>/', delete_episode, name='delete_episode'),
# ]
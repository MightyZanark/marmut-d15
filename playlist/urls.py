from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('', user_playlist, name = 'user_playlist'),
]

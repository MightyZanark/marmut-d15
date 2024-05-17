from django.urls import path

from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('playlist/', playlist, name='playlist'),
    path('playlist/<uuid:id_user_playlist>/', detail_playlist, name='detail_playlist'),
    path('playlist/<uuid:id_user_playlist>/ubah/', ubah_playlist, name='ubah_playlist'),
    path('playlist/<uuid:id_user_playlist>/hapus/', hapus_playlist, name='hapus_playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('playlist/<str:id_user_playlist>/shuffle_play/', shuffle_play, name='shuffle_play'),
    path('playlist/<uuid:id_user_playlist>/tambah_lagu/', tambah_lagu, name='tambah_lagu'),
    path('song/<uuid:id_song>/', detail_lagu, name='detail_lagu'),
    path('chart/', chart_list, name='chart_list'),
    path('chart/<str:chart_id>/', chart_detail, name='chart_detail'),
    path('', user_playlist, name = 'user_playlist'),
]

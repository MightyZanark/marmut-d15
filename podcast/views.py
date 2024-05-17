from django.http import HttpRequest
from django.shortcuts import render

from podcast.utils import get_podcast, get_podcaster, get_genres, get_episodes, \
                            format_duration

# Create your views here.

def play_podcast(request: HttpRequest, podcast_id: str):
    context = {}
    podcast_detail = get_podcast(podcast_id)
    podcaster = get_podcaster(podcast_id)
    genres = get_genres(podcast_id)
    episodes = get_episodes(podcast_id)

    context['podcast'] = podcast_detail[0]
    context['tanggal_rilis'] = podcast_detail[1]
    context['tahun'] = podcast_detail[2]
    context['duration'] = format_duration(podcast_detail[3])
    context['podcaster'] = podcaster
    context['genres'] = [genre[0] for genre in genres]

    for i in range(len(episodes)):
        judul = episodes[i][0]
        deskripsi = episodes[i][1]
        durasi = episodes[i][2]
        tanggal_rilis = episodes[i][3]

        durasi = format_duration(durasi)

        episodes[i] = judul, deskripsi, durasi, tanggal_rilis
    
    context['episodes'] = episodes

    return render(request, 'play_podcast.html', context)

from django.http import HttpRequest, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect

from podcast.utils import get_podcast, get_podcaster, get_genres, get_episodes, \
                            format_duration, create_podcast_db, \
                            create_episode_db, get_podcast_by_podcaster, \
                            delete_episode_db, delete_podcast_db

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


def create_podcast(request: HttpRequest):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")

    if request.method == 'POST':
        judul = request.POST.get('judul', '')
        business = request.POST.get('business', '')
        comedy = request.POST.get('comedy', '')
        sports = request.POST.get('sports', '')
        news = request.POST.get('news', '')
        history = request.POST.get('history', '')
        fiction = request.POST.get('fiction', '')
        music = request.POST.get('music', '')

        genres = [business, comedy, sports, news, history, fiction, music]

        if all(not genre for genre in genres):
            messages.info(request, 'Please select a genre')
            return render(request, 'create_podcast.html', {})
        
        genres = ' '.join(genres).split() # Remove empty genre
        create_podcast_db(judul, genres, request.session.get('user_email'))
        return redirect(reverse('podcast:list_podcast'))

    return render(request, 'create_podcast.html', {})


def create_episode(request: HttpRequest, podcast_id: str):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")
    
    if request.method == 'POST':
        judul = request.POST.get('judul', '')
        deskripsi = request.POST.get('deskripsi', '')
        durasi = request.POST.get('durasi', '')

        create_episode_db(podcast_id, judul, deskripsi, durasi)
        return redirect(reverse('podcast:list_podcast'))

    podcast_name = get_podcast(podcast_id)[0]

    return render(request, 'create_episode.html', {'podcast': podcast_name})


def list_podcast(request: HttpRequest):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")
    
    podcasts = get_podcast_by_podcaster(request.session.get('user_email'))
    for i in range(len(podcasts)):
        data = [*podcasts[i]]
        data[3] = format_duration(data[3])
        podcasts[i] = data

    return render(request, 'list_podcast.html', {'podcasts': podcasts})


def list_episodes(request: HttpRequest, podcast_id: str):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")
    
    episodes = get_episodes(podcast_id)
    for i in range(len(episodes)):
        data = [*episodes[i]]
        data[2] = format_duration(data[2])
        episodes[i] = data
    
    podcast_name = get_podcast(podcast_id)[0]
    
    ctx = {
        'episodes': episodes,
        'podcast': podcast_name,
        'podcast_id': podcast_id
    }
    
    return render(request, 'daftar_episode.html', ctx)


def delete_podcast(request: HttpRequest, podcast_id: str):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")
    
    delete_podcast_db(podcast_id)
    
    return redirect(reverse('podcast:list_podcast'))


def delete_episode(request: HttpRequest, podcast_id: str, episode_id: str):
    is_podcaster = request.session.get('user_type')['is_podcaster']
    if not request.session.get('user_email', None) or not is_podcaster:
        return HttpResponseForbidden("You are not a podcaster")
    
    delete_episode_db(episode_id)
    
    return redirect(reverse('podcast:list_episode', kwargs={'podcast_id': podcast_id}))

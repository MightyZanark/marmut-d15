from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from .utils import *

def list_album(request):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")

    context = get_album(email, is_artist(email))

    return render(request, 'list_album.html', {"list_album": context})

def detail_album(request, album_id):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")
    
    context = get_album_detail(album_id)

    return render(request, 'detail_album.html', {"list_album_lagu": context})

def create_song(request, album_id):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")
    
    genre_list = get_genre()
    artist_list = get_artist()
    songwriter_list = get_songwriter()
    akun_name = get_akun_name(email)
    album_name = get_album_detail(album_id)[0].get("judul_album")

    self_songwriter = []

    if is_artist(email):
        artist_list = [{"email": email, "nama": get_akun_name(email)}]

    if is_songwriter(email):
        self_songwriter = [email]

    context = {
        "akun_name": akun_name,
        "album_name": album_name,
        "genre_list": genre_list,
        "artist_list": artist_list,
        "songwriter_list": songwriter_list
    }
    
    if request.method == 'POST':
        judul = request.POST.get('judul', '')
        artist = request.POST.get('artist', '')
        songwriter = request.POST.getlist('songwriter')
        genre = request.POST.getlist('genre')
        durasi = request.POST.get('durasi', '')

        songwriter = songwriter + self_songwriter

        create_song_db(album_id, judul, artist, songwriter, genre, durasi)

        return redirect(reverse('album:list_album'))

    return render(request, 'create_song.html', {"context": context})

def delete_song(request, album_id, song_id):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")
    
    delete_song_db(song_id)

    return redirect(reverse('album:detail_album', args=[album_id]))

def create_album(request):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")
    

    label_list = get_label()


    
    genre_list = get_genre()
    artist_list = get_artist()
    songwriter_list = get_songwriter()
    akun_name = get_akun_name(email)

    self_songwriter = []

    if is_artist(email):
        artist_list = [{"email": email, "nama": get_akun_name(email)}]

    if is_songwriter(email):
        self_songwriter = [email]

    context = {
        "akun_name": akun_name,
        "genre_list": genre_list,
        "artist_list": artist_list,
        "songwriter_list": songwriter_list,
        "label_list": label_list,
    }
    
    if request.method == 'POST':
        judul_album = request.POST.get('judul_album', ' ')
        label = request.POST.getlist('label')[0]

        judul_lagu = request.POST.get('judul_lagu', '')
        artist = request.POST.get('artist', '')
        songwriter = request.POST.getlist('songwriter')
        genre = request.POST.getlist('genre')
        durasi = request.POST.get('durasi', '')

        songwriter = songwriter + self_songwriter

        create_album_db(judul_album, label, judul_lagu, artist, songwriter, genre, durasi)

        # print(judul_album)
        # print(label)
        # print(judul_lagu)
        # print(artist)
        # print(songwriter)
        # print(genre)
        # print(durasi)

        return redirect(reverse('album:list_album'))

    return render(request, 'create_album.html', {"context": context})


def delete_album(request, album_id):
    email = request.session.get('user_email', None)

    if not email or not is_artist(email) and not is_songwriter(email):
        return HttpResponseForbidden("You are not a songwriter/artist")
    
    delete_album_db(album_id)

    return redirect(reverse('album:list_album'))
    



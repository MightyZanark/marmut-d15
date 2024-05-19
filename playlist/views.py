from datetime import datetime, timezone
from pyexpat.errors import messages
from django.db import connection
from django.http import HttpRequest
from django.shortcuts import redirect, render
import uuid
from playlist.utils import get_charts, get_chart_type, get_chart_song

from django.urls import reverse

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def playlist(request):
    if not request.session.get('user_email'):
        return redirect('authentication:login')

    email = request.session['user_email']
    #print(email +"MASUK HA")

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE email_pembuat = %s", [email])
        playlists = dictfetchall(cursor)

    return render(request, 'playlist.html', {'playlists': playlists})


def detail_playlist(request, id_user_playlist):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
        playlist = dictfetchall(cursor)[0]  

    durasi_menit = playlist['total_durasi']
    jam = durasi_menit // 60
    menit = durasi_menit % 60

    if request.method == 'POST':
        if 'play' in request.POST:
            id_song = request.POST['play']
            timestamp = datetime.now()
            email_pemain = request.session['user_email'] 
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO akun_play_song (email_pemain, id_song, waktu) VALUES (%s, %s, %s)", [email_pemain, id_song, timestamp])
                cursor.execute("UPDATE song SET total_play = total_play + 1 WHERE id_konten = %s", [id_song])
        elif 'delete' in request.POST:
            id_song = request.POST['delete']
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM playlist_song WHERE id_playlist = %s AND id_song = %s", [playlist['id_playlist'], id_song])

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT k.judul, a.nama as artist, k.durasi, s.id_konten as id_song
            FROM playlist_song ps
            JOIN song s ON ps.id_song = s.id_konten
            JOIN konten k ON s.id_konten = k.id
            JOIN artist ar ON s.id_artist = ar.id
            JOIN akun a ON ar.email_akun = a.email
            WHERE ps.id_playlist = %s
        """, [playlist['id_playlist']])
        songs = dictfetchall(cursor)  

    for song in songs:
        durasi_lagu = song['durasi']
        song['jam_lagu'] = durasi_lagu // 60
        song['menit_lagu'] = durasi_lagu % 60

    return render(request, 'detail_playlist.html', {'playlist': playlist, 'songs': songs, 'jam': jam, 'menit': menit})


def shuffle_play(request, id_user_playlist):
    if request.method == 'POST':
        timestamp = datetime.now()
        email_pemain = request.session['user_email'] 
        email_pembuat = request.session['user_email']  

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_playlist FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
            id_playlist = cursor.fetchone()[0]

            cursor.execute("INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu) VALUES (%s, %s, %s, %s)", [email_pemain, id_user_playlist, email_pembuat, timestamp])

            cursor.execute("SELECT id_song FROM playlist_song WHERE id_playlist = %s", [id_playlist])
            songs = cursor.fetchall()

            for song in songs:
                cursor.execute("INSERT INTO akun_play_song (email_pemain, id_song, waktu) VALUES (%s, %s, %s)", [email_pemain, song[0], timestamp])
                cursor.execute("UPDATE song SET total_play = total_play + 1 WHERE id_konten = %s", [song[0]])

        return redirect(reverse('playlist:detail_playlist', args=[id_user_playlist]))


def ubah_playlist(request, id_user_playlist):
    if request.method == 'POST':
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']

        with connection.cursor() as cursor:
            cursor.execute("UPDATE user_playlist SET judul = %s, deskripsi = %s WHERE id_user_playlist = %s", [judul, deskripsi, id_user_playlist])

        return redirect('playlist:playlist')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
        playlist = dictfetchall(cursor)[0] 
    return render(request, 'ubah_playlist.html', {'playlist': playlist})


def hapus_playlist(request, id_user_playlist):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM akun_play_user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
            
            cursor.execute("DELETE FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])

        return redirect('playlist:playlist')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
        playlist = dictfetchall(cursor)[0] 

    return render(request, 'hapus_playlist.html', {'playlist': playlist})


def tambah_playlist(request):
    if not request.session.get('user_email'):
        return redirect('authentication:login')

    if request.method == 'POST':
        email_pembuat = request.session['user_email']
        id_user_playlist = uuid.uuid4()
        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']
        jumlah_lagu = 0
        tanggal_dibuat = datetime.now()
        id_playlist = None
        total_durasi = 0

        with connection.cursor() as cursor:
            id_playlist = uuid.uuid4()
            cursor.execute("INSERT INTO playlist (id) VALUES (%s)", [id_playlist])

            cursor.execute("INSERT INTO user_playlist (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi])

        return redirect('playlist:playlist')

    return render(request, 'tambah_playlist.html')


def tambah_lagu(request, id_user_playlist):
    if not request.session.get('user_email'):
        return redirect('authentication:login')

    if request.method == 'POST':
        id_song = request.POST['song']

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_playlist FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
            id_playlist = cursor.fetchone()[0]

            cursor.execute("SELECT * FROM playlist_song WHERE id_playlist = %s AND id_song = %s", [id_playlist, id_song])
            if cursor.fetchone() is not None:
                return render(request, 'tambah_lagu.html', {'error': 'This song is already in the playlist.'})

            cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s)", [id_playlist, id_song])

        return redirect('playlist:detail_playlist', id_user_playlist=id_user_playlist)

    with connection.cursor() as cursor:
        cursor.execute("SELECT s.id_konten, k.judul, a.nama as artist FROM song s JOIN konten k ON s.id_konten = k.id JOIN artist ar ON s.id_artist = ar.id JOIN akun a ON ar.email_akun = a.email")
        songs = dictfetchall(cursor) 

    return render(request, 'tambah_lagu.html', {'songs': songs})


def detail_lagu(request, id_song):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT k.judul, a.nama as artist, k.durasi, s.id_konten as id_song, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, al.judul as album
            FROM song s
            JOIN konten k ON s.id_konten = k.id
            JOIN artist ar ON s.id_artist = ar.id
            JOIN akun a ON ar.email_akun = a.email
            LEFT JOIN album al ON s.id_album = al.id
            WHERE s.id_konten = %s
        """, [id_song])
        song = dictfetchall(cursor)[0]

        cursor.execute("""
            SELECT genre
            FROM genre
            WHERE id_konten = %s
        """, [id_song])
        genres = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT a.nama
            FROM songwriter sw
            JOIN songwriter_write_song sws ON sw.id = sws.id_songwriter
            JOIN akun a ON sw.email_akun = a.email
            WHERE sws.id_song = %s
        """, [id_song])
        songwriters = [row[0] for row in cursor.fetchall()]

    song['genres'] = genres
    song['songwriters'] = songwriters

    return render(request, 'main_lagu.html', {'song': song})


def main_lagu(request, id_song):
    if request.method == 'POST':
        progress = int(request.POST['progress'])
        if progress > 70:
            timestamp = datetime.now()
            email_pemain = request.session['user_email'] 
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO akun_play_song (email_pemain, id_song, waktu) VALUES (%s, %s, %s)", [email_pemain, id_song, timestamp])
                cursor.execute("UPDATE song SET total_play = total_play + 1 WHERE id_konten = %s", [id_song])

    return redirect(reverse('playlist:detail_lagu', args=[id_song]))


def lagu_ke_playlist(request, id_song):
    if not request.session.get('user_email'):
        return redirect('login')

    email = request.session['user_email']

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE email_pembuat = %s", [email])
        playlists = dictfetchall(cursor)

    if not playlists:
        messages.error(request, "Anda belum membuat playlist. Silakan buat playlist terlebih dahulu.")
        return redirect('song_detail', id_song=id_song)

    return render(request, 'lagu_ke_playlist.html', {'playlists': playlists, 'song_id': id_song})


def submit_lagu_ke_playlist(request, id_song):
    if not request.session.get('user_email'):
        return redirect('login')

    email = request.session['user_email']
    id_user_playlist = request.POST['playlist']

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_playlist FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
        id_playlist = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM playlist_song WHERE id_playlist = %s AND id_song = %s", [id_playlist, id_song])
        if cursor.fetchone() is not None:
            cursor.execute("SELECT judul FROM konten WHERE id = %s", [id_song])
            song_title = cursor.fetchone()[0]
            cursor.execute("SELECT judul FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
            playlist_title = cursor.fetchone()[0]
            return render(request, 'submit_lagu_ke_playlist.html', {'success': False, 'song_title': song_title, 'playlist_title': playlist_title, 'song_id': id_song, 'playlist_id': id_user_playlist})

        cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s)", [id_playlist, id_song])
        cursor.execute("SELECT judul FROM konten WHERE id = %s", [id_song])
        song_title = cursor.fetchone()[0]
        cursor.execute("SELECT judul FROM user_playlist WHERE id_user_playlist = %s", [id_user_playlist])
        playlist_title = cursor.fetchone()[0]

    return render(request, 'submit_lagu_ke_playlist.html', {'success': True, 'song_title': song_title, 'playlist_title': playlist_title, 'song_id': id_song, 'playlist_id': id_user_playlist})


def download_song(request, id_song):
    email_pemain = request.session['user_email'] 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM downloaded_song WHERE id_song = %s AND email_downloader = %s", [id_song, email_pemain])
        song_already_downloaded = cursor.fetchone()
        if song_already_downloaded:
            cursor.execute("SELECT judul FROM konten WHERE id = %s", [id_song])
            song_title = cursor.fetchone()[0]
            return render(request, 'sudah_download.html', {'song': {'judul': song_title}})
        else:
            cursor.execute("INSERT INTO downloaded_song (id_song, email_downloader) VALUES (%s, %s)", [id_song, email_pemain])
            cursor.execute("UPDATE song SET total_download = total_download + 1 WHERE id_konten = %s", [id_song])
            cursor.execute("SELECT judul FROM konten WHERE id = %s", [id_song])
            song_title = cursor.fetchone()[0]
            return render(request, 'sukses_download.html', {'song': {'judul': song_title}})



def chart_list(request: HttpRequest):
    charts = get_charts()
    return render(request, 'chart_list.html', {'charts': charts})


def chart_detail(request: HttpRequest, chart_id: str):
    ctx = {'chart_type': get_chart_type(chart_id)}
    ctx['songs'] = get_chart_song(chart_id)

    return render(request, 'chart_detail.html', ctx)


def user_playlist(request):
    return render(request, 'userPlaylist.html')


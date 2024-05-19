from datetime import date
from uuid import uuid4
from django.db import connection

def get_akun_name(email):
    with connection.cursor() as cursor:
        cursor.execute(f"select nama from akun where email = '{email}'")

        data = cursor.fetchone()[0]
    
    return data

def is_artist(email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM artist WHERE email_akun = %s)",
            [email]
        )
        return cursor.fetchone()[0]
    
def is_songwriter(email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM songwriter WHERE email_akun = %s)",
            [email]
        )
        return cursor.fetchone()[0]
    
def is_label(email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM label WHERE id = %s)",
            [email]
        )
        return cursor.fetchone()[0]
    
def get_album(email, is_artist, is_label):
    with connection.cursor() as cursor:

        if is_label:
            cursor.execute(f"select distinct album.id, judul, label.nama, jumlah_lagu, total_durasi from label, album where label.id='{email}' and album.id_label = label.id")
        else:
            if is_artist:
                cursor.execute(f"select distinct album.id, judul, label.nama as nama_label, jumlah_lagu, total_durasi from artist, song, label, album where artist.email_akun = '{email}' and song.id_artist = artist.id and album.id = song.id_album and album.id_label = label.id;")
            else:
                cursor.execute(f"select distinct album.id, album.judul, label.nama as nama_label, jumlah_lagu, total_durasi from songwriter as sw, song as s, songwriter_write_song as sws, album, label where sw.email_akun = '{email}' and sws.id_songwriter = sw.id and sws.id_song = s.id_konten and s.id_album = album.id and album.id_label = label.id;")

        data = cursor.fetchall()

        daftar_album = []

        for d in data:
            id, judul, label, jumlah, durasi = d

            album = {
                "id": id,
                "judul": judul,
                "label": label,
                "jumlah": jumlah,
                "durasi": durasi,
                "is_label": is_label
            }
            daftar_album.append(album)

        return daftar_album
    
def get_album_detail(album_id):
    with connection.cursor() as cursor:
        cursor.execute(f"select konten.id, album.judul, konten.judul as judul, konten.durasi as durasi, total_play, total_download from album, song, konten where album.id = '{album_id}' and song.id_album = album.id and konten.id = song.id_konten;")
    
        data = cursor.fetchall()

        album_lagu = []

        for d in data:
            konten_id, judul_album, judul, durasi, play, download = d

            lagu = {
                "konten_id": konten_id,
                "judul_album": judul_album,
                "album_id": album_id,
                "judul": judul,
                "durasi": play,
                "play": download,
                "download": durasi
            }
            album_lagu.append(lagu)
        
        return album_lagu
    
def create_song_db(album_id, judul, artist_email, songwriter_email_list, genre_list, durasi):
    with connection.cursor() as cursor:
        konten_id = uuid4()
        tanggal_rilis = date.today()
        tahun = tanggal_rilis.year

        cursor.execute(
            "INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) "
            "VALUES (%s, %s, %s, %s, %s)",
            [konten_id, judul, tanggal_rilis, tahun, durasi]
        )

        cursor.execute(f"select id from artist where artist.email_akun='{artist_email}'")
        artist_id = cursor.fetchone()[0]
            
        cursor.execute(
            "INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download) "
            "VALUES (%s, %s, %s, %s, %s)",
            [konten_id, artist_id, album_id, 0, 0]
        )

        for sw_email in songwriter_email_list:

            cursor.execute(f"select id from songwriter where email_akun='{sw_email}'")
            sw_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO songwriter_write_song (id_songwriter, id_song) "
                "VALUES (%s, %s)",
                [sw_id, konten_id]
            )

        for genre in genre_list:
            cursor.execute(
                "INSERT INTO genre (id_konten, genre) "
                "VALUES (%s, %s)",
                [konten_id, genre]
            )

def delete_song_db(song_id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM konten where id='{song_id}'")

def create_album_db(judul_album, id_label, judul_lagu, artist_email, songwriter_email_list, genre_list, durasi):
    with connection.cursor() as cursor:
        album_id = uuid4()

        cursor.execute(
            "INSERT INTO album (id, judul, jumlah_lagu, id_label, total_durasi) "
            "VALUES (%s, %s, %s, %s, %s)",
            [album_id, judul_album, 0, id_label, 0]
        )


        konten_id = uuid4()
        tanggal_rilis = date.today()
        tahun = tanggal_rilis.year

        cursor.execute(
            "INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) "
            "VALUES (%s, %s, %s, %s, %s)",
            [konten_id, judul_lagu, tanggal_rilis, tahun, durasi]
        )

        cursor.execute(f"select id from artist where artist.email_akun='{artist_email}'")
        artist_id = cursor.fetchone()[0]
            
        cursor.execute(
            "INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download) "
            "VALUES (%s, %s, %s, %s, %s)",
            [konten_id, artist_id, album_id, 0, 0]
        )

        for sw_email in songwriter_email_list:

            cursor.execute(f"select id from songwriter where email_akun='{sw_email}'")
            sw_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO songwriter_write_song (id_songwriter, id_song) "
                "VALUES (%s, %s)",
                [sw_id, konten_id]
            )

        for genre in genre_list:
            cursor.execute(
                "INSERT INTO genre (id_konten, genre) "
                "VALUES (%s, %s)",
                [konten_id, genre]
            )

def delete_album_db(album_id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM album where id='{album_id}'")

def get_genre():
    with connection.cursor() as cursor:
        cursor.execute("select distinct genre from genre")

        data = cursor.fetchall()
        list = [i[0] for i in data]

    return list

def get_artist():
    with connection.cursor() as cursor:
        cursor.execute("select akun.email, akun.nama from akun, artist where akun.email = artist.email_akun")

        data = cursor.fetchall()
        list = [{"email": i[0], "nama": i[1]} for i in data]

    return list

def get_songwriter():
    with connection.cursor() as cursor:
        cursor.execute("select akun.email, akun.nama from akun, songwriter where akun.email = songwriter.email_akun")

        data = cursor.fetchall()
        list = [{"email": i[0], "nama": i[1]} for i in data]

    return list

def get_label():
    with connection.cursor() as cursor:
        cursor.execute("select id, nama from label")

        data = cursor.fetchall()
        list = [{"id": i[0], "nama": i[1]} for i in data]
    
    return list
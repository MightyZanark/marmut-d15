from django.db import connection

def get_charts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM chart")
        return cursor.fetchall()


def get_chart_type(chart_id: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT tipe FROM chart WHERE id_playlist = %s", [chart_id])
        return cursor.fetchone()[0]


def get_chart_song(chart_id: str):
    update_chart_song(chart_id)
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT K.judul, U.nama, K.tanggal_rilis, S.total_play, K.id FROM konten K "
            "JOIN song S ON K.id = S.id_konten "
            "JOIN artist A ON S.id_artist = A.id "
            "JOIN akun U ON A.email_akun = U.email "
            "JOIN playlist_song PS ON S.id_konten = PS.id_song "
            "JOIN chart C ON PS.id_playlist = C.id_playlist "
            "WHERE C.id_playlist = %s ORDER BY S.total_play DESC",
            [chart_id]
        )
        return cursor.fetchall()


def update_chart_song(chart_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_konten FROM song ORDER BY total_play DESC LIMIT 20"
        )
        songs = cursor.fetchall()
        
        cursor.execute(
            "DELETE FROM playlist_song * WHERE id_playlist = %s",
            [chart_id]
        )

        for song in songs:
            cursor.execute(
                "INSERT INTO playlist_song (id_playlist, id_song) "
                "VALUES (%s, %s)",
                [chart_id, song[0]]
            )

from django.db import connection

def get_podcast(podcast_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT judul, tanggal_rilis, tahun, durasi "
            "FROM konten WHERE id = %s",
            [podcast_id]
        )
        return cursor.fetchone()


def get_podcaster(podcast_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT nama FROM akun "
            "WHERE email = (SELECT email_podcaster FROM podcast WHERE id_konten = %s)",
            [podcast_id]
        )
        return cursor.fetchone()[0]


def get_genres(podcast_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT genre FROM genre "
            "WHERE id_konten = %s",
            [podcast_id]
        )
        return cursor.fetchall()


def get_episodes(podcast_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT judul, deskripsi, durasi, tanggal_rilis "
            "FROM episode WHERE id_konten_podcast = %s",
            [podcast_id]
        )
        return cursor.fetchall()


def format_duration(duration: int):
    res = f'{duration % 60} menit'
    if duration > 60:
        res = f'{duration // 60} jam {res}'
    return res

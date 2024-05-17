from uuid import uuid4
from datetime import date

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
            "SELECT judul, deskripsi, durasi, tanggal_rilis, id_episode "
            "FROM episode WHERE id_konten_podcast = %s",
            [podcast_id]
        )
        return cursor.fetchall()


def format_duration(duration: int):
    res = f'{duration % 60} menit'
    if duration > 60:
        res = f'{duration // 60} jam {res}'
    return res


def is_podcaster(podcaster_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM podcaster WHERE email = %s)",
            [podcaster_id]
        )
        return cursor.fetchone()[0]


def create_podcast_db(judul: str, genres: list[str], podcaster: str):
    with connection.cursor() as cursor:
        konten_id = uuid4()
        tanggal_rilis = date.today()
        tahun = tanggal_rilis.year
        
        cursor.execute(
            "INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) "
            "VALUES (%s, %s, %s, %s, 0)",
            [konten_id, judul, tanggal_rilis, tahun]
        )

        cursor.execute(
            "INSERT INTO podcast (id_konten, email_podcaster) "
            "VALUES (%s, %s)",
            [konten_id, podcaster]
        )

        for genre in genres:
            cursor.execute(
                "INSERT INTO genre (id_konten, genre) "
                "VALUES (%s, %s)",
                [konten_id, genre]
            )


def create_episode_db(*attr: tuple[str]):
    with connection.cursor() as cursor:
        episode_id = uuid4()
        tanggal_rilis = date.today()

        cursor.execute(
            "INSERT INTO episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            [episode_id, *attr, tanggal_rilis]
        )


def get_podcast_by_podcaster(podcaster_id: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT K.id, K.judul, COUNT(E.id_episode), K.durasi "
            "FROM konten K FULL JOIN episode E ON K.id = E.id_konten_podcast "
            "WHERE K.id IN (SELECT id_konten FROM podcast WHERE email_podcaster = %s) "
            "GROUP BY K.id",
            [podcaster_id]
        )
        return cursor.fetchall()


def delete_podcast_db(podcast: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM konten * WHERE id = %s",
            [podcast]
        )


def delete_episode_db(episode: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM episode * WHERE id_episode = %s",
            [episode]
        )

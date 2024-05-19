from django.db import connection

def get_royalti():
    with connection.cursor() as cursor:
        
        cursor.execute(
            'select rate_royalti, total_play, k.judul as judul_lagu, alb.judul as judul_album, s.total_download '
            'from artist as a, pemilik_hak_cipta as phc, song as s, royalti as r, konten as k, album as alb ' 
            'where a.id_pemilik_hak_cipta = phc.id and r.id_song = s.id_konten and r.id_pemilik_hak_cipta = phc.id and k.id = s.id_konten and alb.id = s.id_album '
            'UNION '
            'select rate_royalti, total_play, k.judul as judul_lagu, alb.judul as judul_album, s.total_download '
            'from songwriter as sws, pemilik_hak_cipta as phc, song as s, royalti as r, konten as k, album as alb '
            'where sws.id_pemilik_hak_cipta = phc.id and r.id_song = s.id_konten and r.id_pemilik_hak_cipta = phc.id and k.id = s.id_konten and alb.id = s.id_album'
        )

        data = cursor.fetchall()

        cursor.execute(
            """select rate_royalti, total_play, k.judul as judul_lagu, alb.judul as judul_album, s.total_download
from label as l, pemilik_hak_cipta as phc, song as s, royalti as r, konten as k, album as alb
where l.id_pemilik_hak_cipta = phc.id and r.id_song = s.id_konten and r.id_pemilik_hak_cipta = phc.id and k.id = s.id_konten and alb.id = s.id_album;
            """
        )

        data2 = cursor.fetchall()

        daftar_royalti = []

        for d in data:
            rate, play, lagu, album, download = d

            royalti = {
                "lagu": lagu,
                "album": album,
                "play": play,
                "download": download,
                "total_royalti": rate*play
            }
            daftar_royalti.append(royalti)

        for d in data2:
            rate, play, lagu, album, download = d

            royalti = {
                "lagu": lagu,
                "album": album,
                "play": play,
                "download": download,
                "total_royalti": rate*play
            }
            daftar_royalti.append(royalti)

        return daftar_royalti
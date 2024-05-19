from django.db import connection

def akun_dashboard(email):
    with connection.cursor() as cursor:

        nama = None

        if "@" not in email:
            cursor.execute(f"select nama, email, kontak from label where id='{email}'")
            nama,email,kontak = cursor.fetchone()

        if not nama:

            cursor.execute(f"""
                        select akun.email, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, premium.email as is_premium, podcaster.email as is_podcaster, artist.email_akun as is_artist, songwriter.email_akun as is_songwriter 
                        from akun left join premium on akun.email = premium.email left join podcaster on akun.email = podcaster.email left join artist on akun.email = artist.email_akun left join songwriter on akun.email = songwriter.email_akun 
                        where akun.email='{email}';
                        """)
            
            email, nama, gender, tempat, tanggal, kota, prem, pod, art, sw = cursor.fetchone()

            sw = "Songwriter" if sw else ""
            art = "Artist" if art else ""
            pod = "Podcaster" if pod else ""

            role = f"{art} {sw} {pod}"
            prem = "Premium" if prem else "Nonpremium"
            gender = "Laki-laki" if gender else "Perempuan"

            data = {
                "email": email,
                "nama": nama,
                "gender": gender,
                "tempat": tempat,
                "tanggal": tanggal,
                "kota": kota,
                "role": role,
                "prem": prem
            }

        else:
            data = {
                "nama": nama,
                "email": email,
                "kontak": kontak,
                "role": "Label"
            }
    
        return data
    
def get_akun_playlist(email): # untuk semua pengguna
    with connection.cursor() as cursor:
        cursor.execute(f"select * from user_playlist where email_pembuat = '{email}'")

        data = cursor.fetchall()

        daftar_pl = []

        for d in data:
            em, id_usr_pl, judul, desc, jml_lagu, tanggal, id_pl, durasi = d

            pl = {
                "judul": judul,
                "desc": desc,
                "jml_lagu": jml_lagu
            }
            daftar_pl.append(pl)

        return daftar_pl

def get_akun_lagu(email): # untuk artis / songwriter
    with connection.cursor() as cursor:
        cursor.execute(f"select judul, tanggal_rilis, durasi from songwriter as s, songwriter_write_song as sws, konten where email_akun = '{email}' and s.id = sws.id_songwriter and sws.id_song = konten.id;")

        data = cursor.fetchall()

        daftar_lagu = []

        for d in data:
            judul, tanggal, durasi = d

            lagu = {
                "judul": judul,
                "tanggal": tanggal,
                "durasi": durasi
            }
            daftar_lagu.append(lagu)

        cursor.execute(f"select judul, tanggal_rilis, durasi from artist, song, konten where artist.email_akun = '{email}' and artist.id = song.id_artist and song.id_konten = konten.id;")

        data = cursor.fetchall()

        daftar_lagu = []

        for d in data:
            judul, tanggal, durasi = d

            lagu = {
                "judul": judul,
                "tanggal": tanggal,
                "durasi": durasi
            }
            daftar_lagu.append(lagu)
        
    return daftar_lagu

def get_akun_podcast(email): # untuk podcaster
    with connection.cursor() as cursor:
        cursor.execute(f"select judul, tanggal_rilis, durasi from podcaster, podcast, konten where podcaster.email = '{email}' and podcast.email_podcaster = podcaster.email and podcast.id_konten = konten.id;")

        data = cursor.fetchall()

        daftar_pc = []

        for d in data:
            judul, tanggal, durasi = d

            pc = {
                "judul": judul,
                "tanggal": tanggal,
                "durasi": durasi
            }
            daftar_pc.append(pc)

    return daftar_pc

def get_akun_album(email):
    pass
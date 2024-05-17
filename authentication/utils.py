from uuid import uuid4
from random import randint

from django.db import connection
from django.db.utils import InternalError


def create_unverified(*attr: tuple[str]) -> bool:
    # Asumsi input selalu memiliki tipe data yang benar
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                attr
            )
        except InternalError: # Email duplikat
            return False
        
    return True


def create_verified(podcaster: str, artist: str, songwriter: str, *attr: tuple[str]) -> bool:
    # Asumsi input selalu memiliki tipe data yang benar
    pemilik_hak_cipta = True if artist or songwriter else False
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                attr
            )
        except InternalError:
            return False
        
        if podcaster:
            cursor.execute("INSERT INTO podcaster (email) VALUES (%s)", [attr[0]])
        
        if pemilik_hak_cipta:
            pemilik_hak_cipta_id = uuid4()
            rate_royalti = randint(1, 10)
            cursor.execute(
                "INSERT INTO pemilik_hak_cipta (id, rate_royalti) "
                "VALUES (%s, %s)",
                (pemilik_hak_cipta_id, rate_royalti)
            )
        
            if artist:
                artist_id = uuid4()
                cursor.execute(
                    "INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) "
                    "VALUES (%s, %s, %s)",
                    (artist_id, attr[0], pemilik_hak_cipta_id)
                )
                
            if songwriter:
                cursor.execute(
                    "INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) "
                    "VALUES (%s, %s, %s)",
                    (artist_id, attr[0], pemilik_hak_cipta_id)
                )
    
    return True


def create_label(*attr: tuple[str]) -> bool:
    # Asumsi input selalu memiliki tipe data yang benar
    with connection.cursor() as cursor:
        pemilik_hak_cipta_id = uuid4()
        rate_royalti = randint(1, 10)
        cursor.execute(
            "INSERT INTO pemilik_hak_cipta (id, rate_royalti) "
            "VALUES (%s, %s)",
            (pemilik_hak_cipta_id, rate_royalti)
        )

        label_id = uuid4()
        try:
            cursor.execute(
                "INSERT INTO label (id, email, password, nama, kontak, id_pemilik_hak_cipta) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (label_id, *attr, pemilik_hak_cipta_id)
            )
        except InternalError:
            cursor.execute(
                "DELETE FROM pemilik_hak_cipta * WHERE id = %s",
                [pemilik_hak_cipta_id]
            )
            return False

    return True

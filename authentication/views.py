from django.http import HttpRequest
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import connection

from authentication.utils import create_unverified, create_verified, create_label

def register(request: HttpRequest):
    return render(request, 'register.html', {})


def register_pengguna(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        nama = request.POST.get('nama', '')
        gender = request.POST.get('gender', '')
        tempat_lahir = request.POST.get('tempat_lahir', '')
        tanggal_lahir = request.POST.get('tanggal_lahir', '')
        kota_asal = request.POST.get('kota_asal', '')
        podcaster = request.POST.get('podcaster', '')
        artist = request.POST.get('artist', '')
        songwriter = request.POST.get('songwriter', '')

        verified = False if not podcaster and not artist and not songwriter else True

        if not verified:
            success = create_unverified(email, password, nama, gender, tempat_lahir, tanggal_lahir, verified, kota_asal)
            if not success:
                messages.info(request, f'Email {email} has already been used')
                return render(request, 'register_pengguna.html', {})
            
            messages.info(request, 'Successfully registered!')
            return render(request, 'register_pengguna.html', {})
        
        success = create_verified(podcaster, artist, songwriter, email, password, nama, gender, tempat_lahir, tanggal_lahir, verified, kota_asal)
        if not success:
            messages.info(request, f'Email {email} has already been used')
            return render(request, 'register_pengguna.html', {})

    return render(request, 'register_pengguna.html', {})


def register_label(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        nama = request.POST.get('nama', '')
        kontak = request.POST.get('kontak', '')

        success = create_label(email, password, nama, kontak)
        if not success:
            messages.info(request, f'Email {email} has already been used')
            return render(request, 'register_label.html', {})
        
        messages.info(request, 'Successfully registered!')
        return render(request, 'register_label.html', {})

    return render(request, 'register_label.html', {})


def determine_user_type(email, cursor):
    cursor.execute("SELECT email FROM podcaster WHERE email = %s", [email])
    is_podcaster = cursor.fetchone() is not None

    cursor.execute("SELECT email FROM premium WHERE email = %s", [email])
    is_premium = cursor.fetchone() is not None

    cursor.execute("SELECT email_akun FROM artist WHERE email_akun = %s", [email])
    is_artist = cursor.fetchone() is not None

    cursor.execute("SELECT email_akun FROM songwriter WHERE email_akun = %s", [email])
    is_songwriter = cursor.fetchone() is not None

    cursor.execute("SELECT email FROM label WHERE email = %s", [email])
    is_label = cursor.fetchone() is not None

    cursor.execute("SELECT email FROM nonpremium WHERE email = %s", [email])
    is_non_premium = cursor.fetchone() is not None

    user_type = {
        'is_podcaster': is_podcaster,
        'is_premium': is_premium,
        'is_artist': is_artist,
        'is_songwriter': is_songwriter,
        'is_label': is_label,
        'is_non_premium': is_non_premium,
    }

    return user_type


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM akun WHERE email = %s AND password = %s", [email, password])
            user = cursor.fetchone()

            if user is not None:
                request.session['user_email'] = user[0]
                request.session['user_type'] = determine_user_type(email, cursor)
                return redirect('authentication:dashboard')
            else:
                messages.error(request, 'Email or password is incorrect!')
                return redirect('authentication:login')
    else:
        return render(request, 'login.html')
    

def logout(request):
    try:
        del request.session['user_email']
    except KeyError:
        pass
    return redirect('authentication:homepage')

def dashboard(request):
    user_email = request.session.get('user_email') 
    user_type = request.session.get('user_type')
    if user_email is None:
        return redirect('authentication:login')
    else:
        return render(request, 'dashboard.html', {'user_email': user_email, 'user_type': user_type})
    
def homepage(request):
    return render(request, 'homepage.html')
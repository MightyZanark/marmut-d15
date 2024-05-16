from django.http import HttpRequest
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render

from authentication.utils import create_unverified, create_verified, create_label

# Create your views here.

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

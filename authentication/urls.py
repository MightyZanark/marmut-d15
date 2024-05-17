from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register_page'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/label/', register_label, name='register_label'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('homepage/', homepage, name='homepage'),
]

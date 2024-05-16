from django.urls import path
from authentication.views import register, register_pengguna, register_label

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register_page'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/label/', register_label, name='register_label'),
]

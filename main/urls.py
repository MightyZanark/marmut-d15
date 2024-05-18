from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard', dashboard, name='dashboard'),
]


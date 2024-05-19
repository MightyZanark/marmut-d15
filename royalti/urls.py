from django.urls import path

from royalti.views import list_royalti
app_name = 'royalti'

urlpatterns = [
    path('', list_royalti, name='list_royalti'),
]
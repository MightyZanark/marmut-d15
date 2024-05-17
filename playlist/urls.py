from django.urls import path

from playlist.views import chart_list, chart_detail

app_name = 'playlist'

urlpatterns = [
    path('chart/', chart_list, name='chart_list'),
    path('chart/<str:chart_id>/', chart_detail, name='chart_detail'),
]

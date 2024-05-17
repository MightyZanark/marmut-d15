from django.http import HttpRequest
from django.shortcuts import render

from playlist.utils import get_charts, get_chart_type, get_chart_song

# Create your views here.

def chart_list(request: HttpRequest):
    charts = get_charts()
    return render(request, 'chart_list.html', {'charts': charts})


def chart_detail(request: HttpRequest, chart_id: str):
    ctx = {'chart_type': get_chart_type(chart_id)}
    ctx['songs'] = get_chart_song(chart_id)

    return render(request, 'chart_detail.html', ctx)

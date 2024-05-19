from django.shortcuts import render
from .utils import get_royalti

def list_royalti(request):
    context = get_royalti()

    return render(request, 'list_royalti.html', {'context': context})

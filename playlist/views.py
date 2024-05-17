from django.shortcuts import render

# Create your views here.

def user_playlist(request):
    return render(request, 'userPlaylist.html')

from django.shortcuts import redirect, render

from .utils import akun_dashboard, get_akun_lagu, get_akun_playlist, get_akun_podcast

# Create your views here.

def dashboard(request):
    user_email = request.session.get('user_email') 
    user_type = request.session.get('user_type')
    if user_email is None:
        return redirect('authentication:login')
    else:

        user_info = akun_dashboard(user_email)
        playlist = get_akun_playlist(user_email)

        context = {
            "user_info": user_info,
            "user_type": {
                "is_songwriter": user_type.get("is_songwriter"),
                "is_podcaster": user_type.get("is_podcaster")
            },
            "playlist": playlist
        }

        if user_type.get("is_podcaster"):
            podcast = {
                "podcast": get_akun_podcast(user_email)
            }
            
            context = {**context, **podcast}

        if user_type.get("is_songwriter") or user_type.get("is_artist"):
            lagu = {
                "lagu": get_akun_lagu(user_email)
            }
            
            context = {**context, **lagu}

        if user_type.get("is_label"):
            pass

        return render(request, 'dashboard.html', {"user": context})
    
def homepage(request):
    return render(request, 'homepage.html')
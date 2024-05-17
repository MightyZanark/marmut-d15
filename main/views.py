from django.shortcuts import redirect, render

from .utils import akun_dashboard, get_akun_playlist

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
            "playlist": playlist
        }

        # email, pw, nama, gender, tempat, tanggal, iv, kota = data

        # context = {
        #     "email": email,
        #     "nama": nama,
        #     "gender": gender,
        #     "tempat": tempat,
        #     "tanggal": tanggal,
        #     "kota": kota
        # }

        return render(request, 'dashboard.html', {"user": context})
    
def homepage(request):
    return render(request, 'homepage.html')
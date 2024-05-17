from django.shortcuts import redirect, render

# Create your views here.

def dashboard(request):
    user_email = request.session.get('user_email') 
    user_type = request.session.get('user_type')
    if user_email is None:
        return redirect('authentication:login')
    else:
        return render(request, 'dashboard.html', {'user_email': user_email, 'user_type': user_type})
    
def homepage(request):
    return render(request, 'homepage.html')
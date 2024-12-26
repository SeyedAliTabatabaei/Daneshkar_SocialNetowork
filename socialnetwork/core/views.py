from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Profile


@login_required
def home(request):
    try:
        profiles = Profile.objects.get(user=request.user)
    except:
        profiles = None
    return render(request, 'home.html', {'profile':profiles})

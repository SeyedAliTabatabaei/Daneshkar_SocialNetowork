from .models import Profile
#from django.contrib.auth.decorators import login_required


def profilepic(request):
    if not request.user.is_authenticated:
        return {'profilepic': None}
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    return {'profilepic': profile}
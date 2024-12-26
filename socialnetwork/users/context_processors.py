from .models import Profile

def profilepic(request):
    if not request.user.is_authenticated:
        return {'profilepic': None}
    try:
        profile = Profile.objects.get(user=request.user)
    except profile.DoesNotExist:
        profile = None
    return {'profilepic': profile}
from .models import Profile
from .models import Post
#from django.contrib.auth.decorators import login_required


def profilepic(request):
    profiles = Profile.objects.all()
    allposts = Post.objects.all()
    if not request.user.is_authenticated:
        return {'profilepic': None, 'profilepics': profiles}
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    return {'profilepic': profile,'profilepics':profiles,'allposts':allposts}
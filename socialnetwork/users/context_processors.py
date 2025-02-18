from .models import Profile,Post,Reaction



def profilepic(request):
    profiles = Profile.objects.all()
    allposts = Post.objects.all()

    if not request.user.is_authenticated:
        return {'profilepic': None, 'profilepics': profiles}
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    return {'profilepic': profile,'profilepics':profiles,'allposts':allposts,}

def reaction(request):
    allposts = Post.objects.all()
    if(request.user.is_authenticated):
      reactions = Reaction.objects.filter(user=request.user)
    else:
        reactions = None
    return {'reactions':reactions,'allposts':allposts}
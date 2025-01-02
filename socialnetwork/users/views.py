from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.utils.timezone import now

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = f"{user} عزیز شما با موفقیت وارد شدید"
            print(response)
            return redirect('../profile/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, post=post)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm(post=post)

    comments = post.comments.filter(parent__isnull=True) 
    replies = post.comments.filter(parent__isnull=False) 

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'replies': replies,
        'form': form,
    })
def user_profile(request,user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        followings = Follow.objects.filter(follower = request.user, following = user_id ).values_list("following")
        if followings.count() >= 1:
            isfollow = True
        else:
            isfollow = False
    else:
        isfollow = False
    return render(request, 'user_profile.html',{'user':user,'userid':user_id,'isfollow':isfollow})

def search_users(request):
    form = UserSearchForm()
    results = None

    if request.GET.get('query'): 
        query = request.GET['query']
        results = User.objects.filter(username__icontains=query) 

    return render(request, 'search.html', {'form': form, 'results': results})


@login_required


def profile_view(request):
    try:
        profiledata = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profiledata = None
    if request.method == 'POST':
        submitbutton = request.POST.get("submit_button")
        if submitbutton == "form2":
            form2 = ProfileImage(request.POST, request.FILES, instance=profiledata)
            if form2.is_valid():
                savepic = form2.save(commit=False)
                savepic.user = request.user
                savepic.save()
                return redirect("profile")
            else:
                form2 = ProfileImage(instance=profiledata)
        if submitbutton == "form1":
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save() 
                messages.success(request, 'اطلاعات پروفایل شما با موفقیت ذخیره شد.')
                return redirect('profile')  
    else:
        form = ProfileForm(instance=request.user)
        form2 = ProfileImage(instance=profiledata)
    try:
        form
    except NameError:
        pass
    else:
        try:
            form2
        except NameError:
            return render(request, 'profile.html', {'form': form})
        else:
            return render(request, 'profile.html', {'form': form,'form2':form2, 'profiledata':profiledata})

def write_view(request):
    if request.method == 'POST':
        post_form  = postform(request.POST)
        tag_form = tagform(request.POST)
        if 'submit_tag' in request.POST:
            if tag_form.is_valid():
                tag_form.save()
        elif 'submit_post' in request.POST:
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
                if post_form.cleaned_data['tags']:  
                    post_form.save_m2m()  
               
            return HttpResponse("پست منتشر شد")
        else:
            print(post_form.errors)
    else:
        post_form = postform()
        tag_form = tagform()
    return render(request, 'write.html', {'post_form':post_form,'tag_form':tag_form})

def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    allposts = Post.objects.filter(tags=tag).order_by('-created_at')
    if request.user.is_authenticated:
        isfollow = FollowTag.objects.filter(tag=tag_id).values_list("tag")
        if isfollow.count() >= 1:
            isfollow = True
        else:
            isfollow = False
    else:
        isfollow = False

    posts = []
    for post in allposts:
        posts.append({
            'post': post,
            'time_ago': f"{translate_timesince(post.created_at)}"
        }) 
    return render(request, 'tag_posts.html', {'tag': tag, 'posts': posts,'isfollow':isfollow})

@login_required
def follow_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    user = request.user
    if not FollowTag.objects.filter(user=user, tag=tag).exists():
        FollowTag.objects.create(user=user, tag=tag)
    return redirect('tag_posts', tag_id=tag.id)
def unfollow_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    user = request.user
    if FollowTag.objects.filter(user=user, tag=tag).exists():
        FollowTag.objects.filter(user=user, tag=tag).delete()
    return redirect('tag_posts', tag_id=tag.id)

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:  
        post.delete()
        return redirect('home')
    else:
        return redirect('home')

def ajax_search_users(request):
    query = request.GET.get('query', '') 
    results = []
    if query:
        users = User.objects.filter(username__icontains=query)[:10] 
        results = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'results': results})


def reaction(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        reaction_type = request.POST.get("reaction_type")
        reaction, created = Reaction.objects.get_or_create(user=request.user, post=post)

        if not created and reaction.reaction_type == reaction_type:
            reaction.delete()
            return JsonResponse({'status': 'removed'})
        
        reaction.reaction_type = reaction_type
        reaction.save()

        return JsonResponse({'status': 'added', 'reaction_type': reaction_type, 
                             'likes_count': post.likes_count(),
                             'dislikes_count': post.dislikes_count()})
    
def translate_timesince(time_diff):
    english_time = timesince(time_diff,now())

    translated_time = (
        english_time.replace("minutes", "دقیقه")
        .replace("minute", "دقیقه")
        .replace("hours", "ساعت")
        .replace("hour", "ساعت")
        .replace("days", "روز")
        .replace("day", "روز")
        .replace("weeks", "هفته")
        .replace("week", "هفته")
    )
    return f"{translated_time} پیش"

def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('user_profile', user_id=user_id)

def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('user_profile', user_id=user_id)

def followings(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    allposts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    posts = []
    for post in allposts:
        posts.append({
            'post': post,
            'time_ago': f"{translate_timesince(post.created_at)}"
        }) 
    return render(request, 'followings.html', {'posts': posts})


@login_required
def followed_tags_posts(request):
    user = request.user
    followed_tags = FollowTag.objects.filter(user=user).values_list('tag', flat=True)
    following = Tag.objects.filter(id__in=followed_tags)
    allposts = Post.objects.filter(tags__id__in=followed_tags).distinct().order_by('-created_at')
    posts = []
    for post in allposts:
        posts.append({
            'post': post,
            'time_ago': f"{translate_timesince(post.created_at)}"
        }) 
    return render(request, 'followed_tags_posts.html', {'posts': posts,'following':following})
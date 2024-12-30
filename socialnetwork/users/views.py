from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import *
from .models import Profile,Post,Comment
from django.contrib.auth.models import User

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
    return render(request, 'user_profile.html',{'user':user,'userid':user_id},)

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
        form = postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponse("پست منتشر شد")
        else:
            print(form.errors)
    else:
        form = postform()
    return render(request, 'write.html', {'form':form})


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
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import SignupForm,LoginForm,ProfileForm,ProfileImage
from .models import Profile

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        form2 = ProfileImage(request.POST, request.FILES,   )
        if form2.is_valid():
            savepic = form2.save(commit=False)
            savepic.user = request.user
            savepic.save()
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'اطلاعات پروفایل شما با موفقیت ذخیره شد.')
            return redirect('profile')  
    else:
        form = ProfileForm(instance=request.user)
        form2 = ProfileImage(instance=request.user)
    return render(request, 'profile.html', {'form': form,'form2':form2})

#def profileimage_view(request):


   # return render(request, 'profile.html', {'form2': form, 'profile': profile})

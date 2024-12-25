from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignupForm,LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return redirect('login/')
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


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})
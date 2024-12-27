from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Post,Profile


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts':posts})


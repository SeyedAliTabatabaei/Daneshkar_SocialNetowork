from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Post,Profile
from django.utils.timesince import timesince
from django.utils.timezone import now

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

def home(request):
    allposts = Post.objects.all().order_by('-created_at')
    current_time = now()

    posts = []
    for post in allposts:
        posts.append({
            'post': post,
            'time_ago': f"{translate_timesince(post.created_at)}"
        })  
        
    return render(request, 'home.html', {'posts':posts})


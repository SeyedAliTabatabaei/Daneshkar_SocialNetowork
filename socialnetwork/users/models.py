from django.db import models
from django.contrib.auth.models import User
#from ckeditor.fields import RichTextField




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default="profile_images/default.png", blank=True, null=True)
    bio = models.TextField(max_length=100,blank=True, null=True)

class Post(models.Model):
    title = models.CharField(max_length=200) 
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts") 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    is_published = models.BooleanField(default=True) 

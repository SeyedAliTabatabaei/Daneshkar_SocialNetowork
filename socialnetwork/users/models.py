from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class FollowTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('user', 'tag') 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default="profile_images/default.png", blank=False, null=False)
    bio = models.TextField(max_length=100,blank=True, null=True)

class Post(models.Model):
    title = models.CharField(max_length=200) 
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts") 
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    is_published = models.BooleanField(default=True) 
    
    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')


class Reaction(models.Model):
    reactions= [('like', 'Like'),('dislike', 'Dislike'),]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=reactions)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        unique_together = ('user', 'post')

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following')
    
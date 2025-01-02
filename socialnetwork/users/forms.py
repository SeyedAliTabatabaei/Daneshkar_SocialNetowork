from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',]

    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':' نام کاربری خود را وارد کنید(برای مثال : ahmad)','class':'form-control'}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder':' ایمیل خود را وارد کنید (برای مثال: ahmad@example.com)','class':'form-control'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(
        attrs={'placeholder':'گذرواژه را وارد کنید','class':'form-control'}
    ))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(
        attrs={'placeholder':'تکرار گذرواژه را وارد کنید','class':'form-control'}
    ))
    error_messages = {
      'password_mismatch':'تکرار گذرواژه با گذرواژه یکی نمی باشد',
    }
class LoginForm(AuthenticationForm):
    username = forms.CharField(label=("نام کاربری"),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کاربری'}))
    password = forms.CharField(label=("گذرواژه"),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'گذرواژه را وارد کنید'}))
    error_messages = {
        'invalid_login':"لطفا نام کاربری و رمزعبور خود را به درستی وارد کنید",
        'password_mismatch':'تکرار گذرواژه با گذرواژه یکی نمی باشد',
    }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name', 'last_name']   
        labels = {
            'username':'نام کاربری',
            'email':'ایمیل',
            'first_name':'نام',
            'last_name':'نام خانوادگی',
            
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'disabled':'disabled',
            }),
            'email': forms.TextInput(attrs={
                'class':'form-control',
                'disabled':'disabled',
            }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control',
                'disabled':'disabled',
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control',
                'disabled':'disabled',
            }),
        }

class ProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','bio']
        
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio':forms.Textarea(attrs={'class': 'form-control','placeholder':'بیوگرافی'})
        }

class postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content',]
        labels={
            'title':'عنوان',
            'content':'',
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels={
            'content':'',
        }
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','placeholder':'نظر خود را وارد کنید'})
        }
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None) 
        super().__init__(*args, **kwargs)
    def save(self, user, *args, **kwargs):
        comment = super().save(commit=False)
        comment.user = user
        comment.post = self.post
        parent_comment_id = self.cleaned_data.get('parent_comment_id')
        
        if parent_comment_id:
            comment.parent = Comment.objects.get(id=parent_comment_id)
        
        comment.save()
        return comment
    
class UserSearchForm(forms.Form):
    query = forms.CharField(
            max_length=150,
            label="نام کاربر",
            widget=forms.TextInput(attrs={'placeholder': 'نام کاربر را وارد کنید...'})
        )

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
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
        fields = ['profile_image',]
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

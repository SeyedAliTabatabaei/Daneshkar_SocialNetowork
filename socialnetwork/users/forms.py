from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            "email":"ایمیل",
        }
    username = forms.CharField(label=("نام کاربری"))
    password1 = forms.CharField(label=("گذرواژه"),widget=forms.PasswordInput(
        attrs={'placeholder':'گذرواژه را وارد کنید'}
    ))
    password2 = forms.CharField(label=(" تکرار گذرواژه "),widget=forms.PasswordInput(
        attrs={'placeholder':'تکرار گذرواژه را وارد کن'}
    ))
class LoginForm(AuthenticationForm):
    username = forms.CharField(label=("نام کاربری"),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کاربری'}))
    password = forms.CharField(label=("گذرواژه"),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'گذرواژه را وارد کنید'}))
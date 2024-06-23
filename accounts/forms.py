from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "avatar")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'bio', 'avatar']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Repeat New Password", widget=forms.PasswordInput)


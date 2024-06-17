from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don’t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_home')
                    else:
                        return redirect('user_shelf')
        elif 'register' in request.POST:
            registration_form = RegistrationForm(request.POST, request.FILES)
            if registration_form.is_valid():
                registration_form.save()
                return redirect('login_register')
    else:
        login_form = AuthenticationForm()
        registration_form = RegistrationForm()

    return render(request, 'login_register.html', {
        'login_form': login_form,
        'registration_form': registration_form
    })

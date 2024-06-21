from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import UserUpdateForm, CustomPasswordChangeForm, CustomUserCreationForm


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
            registration_form = CustomUserCreationForm(request.POST, request.FILES)
            if registration_form.is_valid():
                user = registration_form.save(commit=False)
                if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
                user.save()
                return redirect('login_register')
    else:
        login_form = AuthenticationForm()
        registration_form = CustomUserCreationForm()

    return render(request, 'login_register.html', {
        'login_form': login_form,
        'registration_form': registration_form
    })


@login_required
def account_settings(request):
    if request.method == 'POST':
        if 'update_details' in request.POST:
            user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('account_settings')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                return redirect('account_settings')
        elif 'delete_account' in request.POST:
            user = request.user
            user.delete()
            return redirect('login_register')
        elif 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
            request.user.save()
            return redirect('account_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'account_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login_register')

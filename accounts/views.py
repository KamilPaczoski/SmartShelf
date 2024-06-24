from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import UserUpdateForm, CustomPasswordChangeForm, CustomUserForm
from .models import Penalty


def login_register(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) if 'login' in request.POST else CustomUserForm(request.POST,
                                                                                                    request.FILES)
        if form.is_valid():
            if 'login' in request.POST:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('admin_home' if user.is_staff else 'user_shelf')
            else:
                user = form.save(commit=False)
                user.avatar = request.FILES.get('avatar', user.avatar)
                user.save()
                return redirect('login_register')
    else:
        login_form, registration_form = AuthenticationForm(), CustomUserForm()

    return render(request, 'login_register.html', {'login_form': login_form, 'registration_form': registration_form})


@login_required
def account_settings(request):
    user = request.user
    penalties = Penalty.objects.filter(user=user)
    user_form = UserUpdateForm(request.POST, request.FILES, instance=user) if request.method == 'POST' else UserUpdateForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user, data=request.POST) if request.method == 'POST' else CustomPasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'update_details' in request.POST and user_form.is_valid():
            user_form.save()
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
        elif 'delete_account' in request.POST:
            user.delete()
        elif 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()
        return redirect('account_settings')

    return render(request, 'account_settings.html', {
        'user_form': user_form,
        'password_form': password_form,
        'penalties': penalties
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login_register')

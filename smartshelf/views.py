from django.shortcuts import redirect


def startup(request):
    return redirect('login_register')

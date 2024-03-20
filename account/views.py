from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            error_message = 'Invalid phone number or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


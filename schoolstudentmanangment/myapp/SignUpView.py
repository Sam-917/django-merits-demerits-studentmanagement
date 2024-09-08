from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm  

def admin_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True 
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Check if the user is an admin
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid login credentials or not an admin.')
    return render(request, 'login.html')

@login_required
def admin_home(request):
    if not request.user.is_staff:  # Ensure only admins can access
        return HttpResponse('You are not authorized to view this page.')
    return render(request, 'admin/dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def forgot_password(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = f"{settings.FRONTEND_URL}/reset/{uid}/{token}/"
                    
                    subject = "Password Reset Requested"
                    message = render_to_string('password_reset_email.html', {
                        'user': user,
                        'reset_url': reset_url,
                    })
                    
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                
                messages.success(request, 'Password reset email has been sent.')
                return redirect('admin_login')
            else:
                messages.error(request, 'No account found with this email.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    password_reset_form = PasswordResetForm()
    return render(request, 'forgot-password.html', {'form': password_reset_form})


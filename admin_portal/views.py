from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pages.models import Jobs, Events, Invoice, Ticket  # Use existing models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request, 'admin_portal/dashboard.html')

@login_required
def jobs_view(request):
    jobs = Jobs.objects.all()
    return render(request, 'admin_portal/jobs.html', {'jobs': jobs})

@login_required
def events_view(request):
    events = Events.objects.all()
    return render(request, 'admin_portal/events.html', {'events': events})

@login_required
def invoices_view(request):
    invoices = Invoice.objects.all()
    return render(request, 'admin_portal/invoices.html', {'invoices': invoices})

def login_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            request.session['login_email'] = email
            return redirect('admin_login_password')
        else:
            messages.error(request, "Email not found.")
    return render(request, 'admin_portal/login_email.html')


def login_password(request):
    email = request.session.get('login_email')
    if not email:
        return redirect('admin_login_email')

    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=User.objects.get(email=email).username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or permission denied.")
    return render(request, 'admin_portal/login_password.html', {'email': email})
from django.contrib.auth import logout

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login_email')

def reset_password_view(request):
    return render(request, 'admin_portal/reset_password.html')
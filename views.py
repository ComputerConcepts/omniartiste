from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import Contact, Invoice

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        Contact.objects.create(name = name, email = email, message = message)
    return render(request, "contact.html")

def sitemap(request):
    return HttpResponse(open('templates/sitemap.xml').read(), content_type='text/xml')

def events(request):
    return render(request, "events.html")

def buy_now(request):
    return render(request, "buy_now.html")

def payment_for_tickets(request):
    if request.method == 'POST':
        # Retrieve the form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        tickets = int(request.POST.get('tickets'))

        # Example: Calculate the total amount (for example, $50 per ticket)
        ticket_price = 50
        total_amount = tickets * ticket_price

        # Render the payment form and pass the retrieved data
        return render(request, 'payment_for_tickets.html', {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'tickets': tickets,
            'total_amount': total_amount
        })

    # If the request method is GET, simply render the page (or redirect if necessary)
    return render(request, 'payment_for_tickets.html')

def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        #validate this code ,insert logic 
        return render(request, 'email_verification_success.html')
    return render(request, 'verify_email.html')

def email_verification_success(request):
    return render(request, 'email_verification_success.html')

def payment_successful(request):
    return render(request, 'payment_successful.html')

def payment_failure(request):
    return render(request, 'payment_failure.html')

def ticket_verification_failure(request):
    context = {
        'invoice_id': 'INV123456789',
        'ticket_id': 'TICKET987654321',
        'ticket_status': 'Ticket does not exist'
    }
    return render(request, 'ticket_verification_failure.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to homepage after successful login
        else:
            # If authentication fails, display an error message
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Log the user in after signing up
        return redirect('index')
    return render(request, "signup.html")

def invoices(request):
    # Retrieve all invoices from the Invoice model
    invoices = Invoice.objects.all()
    
    # Pass the invoices to the template
    return render(request, 'invoices.html', {'invoices': invoices})

def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=True,
                email_template_name='password_reset_email.html',
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, "forgot_password.html", {'form': form})
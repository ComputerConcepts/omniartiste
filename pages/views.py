# Django imports
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth import authenticate, login
from .models import Invoice, Events, Contact, Ticket, Jobs
import stripe
from .forms import ApplicantForm
from django.core.mail import EmailMessage
import random
import uuid
from django.core.files.storage import FileSystemStorage


# Stripe API key setup
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def jobs(request):
    jobs = Jobs.objects.all()
    return render(request, "jobs.html",{"jobs":jobs})

def jobDetail(request, job_id):
    job = Jobs.objects.get(id=job_id)
    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.job = job
            applicant.save()
            return redirect('jobs')
    else:
        form = ApplicantForm()
    return render(request, "jobDetail.html", {"job": job, "form": form})

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        Contact.objects.create(name=name, email=email, message=message)
    return render(request, "contact.html")


def sitemap(request):
    with open('templates/sitemap.xml') as sitemap_file:
        return HttpResponse(sitemap_file.read(), content_type='text/xml')


def events(request):
    events = Events.objects.all()
    return render(request, "events.html", context={"events": events})


def create_payment_intent(amount, currency='usd', metadata=None):
    try:
        return stripe.PaymentIntent.create(
            amount=amount,  # Amount in cents
            currency=currency,
            payment_method_types=['card'],
            metadata=metadata or {},
        )
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        raise e


def buy_now(request, event_id):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        tickets = int(request.POST.get('tickets', 0))

        if tickets <= 0:
            return render(request, 'buy_now.html', {'error': 'Invalid number of tickets.'})

        # Generate and send OTP
        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        subject = 'Your Email Verification Code'
        message = f'Dear {first_name},\n\nYour OTP for email verification is: {otp}\n\nThank you for purchasing tickets!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # Save user details and OTP in the session
        request.session['otp'] = otp
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['numTickets'] = tickets
        request.session['event_id'] = str(event_id)

        # Redirect to the OTP verification page
        return redirect('verify_email')

    return render(request, 'buy_now.html')


def payment_successful(request):
    payment_intent_id = request.session.get('payment_intent_id')
    if not payment_intent_id:
        return render(request, 'payment_failure.html', {'error': 'Payment intent not found.'})

    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if payment_intent['status'] == 'succeeded':
            invoice = Invoice.objects.get(payment_intent_id=payment_intent_id)
            invoice.paid = True
            invoice.save()

            return render(request, 'payment_successful.html', {'purchase': invoice})
        else:
            return render(request, 'payment_failure.html', {'error': f'Payment status: {payment_intent["status"]}'})
    except (stripe.error.StripeError, Invoice.DoesNotExist) as e:
        return render(request, 'payment_failure.html', {'error': str(e)})


def verify_email(request):
    if request.method == 'POST':
        user_otp = request.POST.get('verification_code')
        session_otp = request.session.get('otp')

        if user_otp == session_otp:
            # OTP verified, clear the session and proceed
            del request.session['otp']  # Remove OTP after successful verification
            return redirect('payment_for_tickets')
        else:
            # OTP mismatch
            return render(request, 'verify_email.html', {'error': 'Invalid OTP. Please try again.'})

    return render(request, 'verify_email.html')

def email_verification_success(request):
    return render(request, 'email_verification_success.html')

def ticket_verification_failure(request):
    context = {
        'invoice_id': 'INV123456789',
        'ticket_id': 'TICKET987654321',
        'ticket_status': 'Ticket does not exist'
    }
    return render(request, 'ticket_verification_failure.html', context)

def payment_for_tickets(request):
    numtickets = request.session.get('numTickets', 1)
    email = request.session.get('email', 'anonymous@example.com')
    event_id = request.session.get('event_id')
    eventNew = Events.objects.get(id = event_id)
    ticket_price = eventNew.cost
    total_amount = numtickets * ticket_price * 100  # Convert to cents

    try:
        payment_intent = create_payment_intent(
            amount=total_amount,
            currency='usd',
            metadata={'email': email, 'tickets': numtickets}
        )

        request.session['payment_intent_id'] = payment_intent['id']

        invoice = Invoice.objects.create(
            first_name=request.session.get('first_name', 'Unknown'),
            last_name=request.session.get('last_name', 'Unknown'),
            email=email,
            payment_intent_id=payment_intent['id'],
            cost = total_amount/100,
            numTickets = numtickets,
            event = str(event_id)
        )
                # Generate and assign tickets to the invoice
        for _ in range(numtickets):
            ticket = Ticket.objects.create(
                event=eventNew,
                email=email,
            )
            invoice.tickets.add(ticket)

        return render(request, 'payment_for_tickets.html', {
            'client_secret': payment_intent['client_secret'],
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'invoice':invoice,
        })
    except stripe.error.StripeError as e:
        return render(request, 'payment_failure.html', {'error': str(e)})


def payment_failure(request):
    return render(request, 'payment_failure.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')
    return render(request, "signup.html")


def invoices(request):
    invoices = Invoice.objects.all()
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

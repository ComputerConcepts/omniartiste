import stripe
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, TicketPurchase
from django.shortcuts import render, redirect
from django.conf import settings
from .models import TicketPurchase


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency='usd', metadata=None):
    """
    Create a Stripe PaymentIntent
    """
    try:
        return stripe.PaymentIntent.create(
            amount=amount,  # Amount in cents
            currency=currency,
            payment_method_types=['card'],
            metadata=metadata or {},
        )
    except stripe.error.StripeError as e:
        # Log or handle the Stripe error
        print(f"Stripe error: {e}")
        raise e


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
    if request.method == 'POST':
        # Collect user details and redirect to payment page
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        tickets = int(request.POST.get('tickets', 0))

        # Validate ticket count
        if tickets <= 0:
            return render(request, 'buy_now.html', {'error': 'Invalid number of tickets.'})

        # Save the user data in session (temporary storage)
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email
        request.session['tickets'] = tickets

        # Redirect to the payment page
        return redirect('payment_for_tickets')

    # For GET requests, render the ticket purchase form
    return render(request, 'buy_now.html')


# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import TicketPurchase

def payment_successful(request):
    payment_intent_id = request.session.get('payment_intent_id')

    if not payment_intent_id:
        print("Error: PaymentIntent ID is missing from the session.")
        return render(request, 'payment_failure.html', {'error': 'Payment intent not found.'})

    try:
        # Retrieve the PaymentIntent from Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Check if the payment was successful
        if payment_intent['status'] == 'succeeded':
            # Retrieve the TicketPurchase object
            ticket_purchase = TicketPurchase.objects.get(payment_intent_id=payment_intent_id)

            # Mark the purchase as paid
            ticket_purchase.paid = True
            ticket_purchase.save()
            print("Database Updated for PaymentIntent:", ticket_purchase)

            # Render the success page with purchase details
            return render(request, 'payment_successful.html', {'purchase': ticket_purchase})

        else:
            print(f"Payment status not succeeded: {payment_intent['status']}")
            return render(request, 'payment_failure.html', {'error': f'Payment status: {payment_intent["status"]}'})
    except stripe.error.StripeError as e:
        print(f"Stripe API error: {e}")
        return render(request, 'payment_failure.html', {'error': str(e)})
    except TicketPurchase.DoesNotExist:
        print(f"No matching TicketPurchase found for PaymentIntent ID: {payment_intent_id}")
        return render(request, 'payment_failure.html', {'error': 'Ticket purchase not found.'})


def payment_for_tickets(request):
    # Retrieve data from session
    tickets = request.session.get('tickets', 1)
    email = request.session.get('email', 'anonymous@example.com')
    ticket_price = 50
    total_amount = tickets * ticket_price * 100  # Convert to cents

    try:
        # Create the PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency='usd',
            payment_method_types=['card'],
            metadata={
                'email': email,
                'tickets': tickets,
            }
        )

        # Save the PaymentIntent ID in the session
        request.session['payment_intent_id'] = payment_intent['id']

        # Create a TicketPurchase object in the database
        TicketPurchase.objects.create(
            first_name=request.session.get('first_name', 'Unknown'),
            last_name=request.session.get('last_name', 'Unknown'),
            email=email,
            tickets=tickets,
            payment_intent_id=payment_intent['id'],  # Save the PaymentIntent ID
        )

        # Render the payment page
        return render(request, 'payment_for_tickets.html', {
            'client_secret': payment_intent['client_secret'],
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })

    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return render(request, 'payment_failure.html', {'error': str(e)})


def payment_failure(request):
    return render(request, 'payment_failure.html')

def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        #validate this code ,insert logic 
        return render(request, 'email_verification_success.html')
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


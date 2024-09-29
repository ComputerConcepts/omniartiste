from django.shortcuts import render, HttpResponse, redirect
from .models import Contact

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        Contact.objects.create(name=name, email=email, message=message)
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

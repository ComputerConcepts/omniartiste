import os
import sys
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import django

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omniartiste.settings')
django.setup()
from pages.models import Invoice, Events

# Add the directory containing the 'pages' module to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def send_email_task():
    logging.info("Sending invoice emails...")
    invoices = Invoice.objects.filter(sent=False)
    for invoice in invoices:
        event = Events.objects.get(id = invoice.event)
        html_content = render_to_string('email/invoice.html', {"invoice": invoice, "event":event})
        email = EmailMultiAlternatives(
            subject="Thank you for your purchase",
            body=str(invoice.id),
            to=[invoice.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        invoice.sent = True
        invoice.save()
    logging.info("Emails sent successfully.")


def main():
    send_email_task()

if __name__ == "__main__":
    main()

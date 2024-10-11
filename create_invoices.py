import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omniartiste.settings')  # Replace with your project name
django.setup()

# Now import the required models
from django.contrib.auth.models import User
from pages.models import Invoice  # Replace 'pages' with your app name

# Create or get a user
user, created = User.objects.get_or_create(username='Vyshnavi', email='vyshnavi@example.com')
if created:
    user.set_password('testpassword')
    user.save()

# Create some dummy invoices
Invoice.objects.create(user=user, amount=200.75, status='Unpaid')

# Output for verification
print(f"User: {user.username}")
invoices = Invoice.objects.filter(user=user)
for invoice in invoices:
    print(f"Invoice {invoice.id} - Amount: {invoice.amount}, Status: {invoice.status}")

#python manage.py create_invoices.py
#python manage.py makemigrations


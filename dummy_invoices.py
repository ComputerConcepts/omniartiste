from pages.models import Invoice
import uuid
# Create a sample invoice
invoice1 = Invoice.objects.create(
    new_id=uuid.uuid4(),  # Generate a UUID
    email='testuser@example.com',  # Replace with your email
    cost=150,
    verified=True,
    first_name='Test',
    last_name='User'
)

invoice2 = Invoice.objects.create(
    new_id=uuid.uuid4(),
    email='anotheruser@example.com',
    cost=200,
    verified=False,
    first_name='Another',
    last_name='User'
)

# Print the newly created invoices
print(invoice1)
print(invoice2)
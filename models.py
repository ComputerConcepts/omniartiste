from django.db import models
from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link invoice to the user
    date = models.DateTimeField(auto_now_add=True)  # Invoice creation date
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the invoice
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])  # Status of invoice

    def __str__(self):
        return f"Invoice {self.id} for {self.user.username} - {self.status}"

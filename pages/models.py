from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class TicketPurchase(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    tickets = models.PositiveIntegerField(default=1)
    payment_intent_id = models.CharField(max_length=200, unique=True)  # Must match Stripe's ID
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.tickets} Tickets"

    class Meta:
        ordering = ['-created_at']
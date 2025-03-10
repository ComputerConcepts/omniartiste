from django.contrib import admin
from pages.models import Contact, Events, Ticket, Invoice, Applicant
from django.db.models import Func, UUIDField
import uuid

from django.contrib import admin
from .models import Contact, Events, Ticket, Invoice, Jobs

class TicketInline(admin.TabularInline):
    model = Invoice.tickets.through  # Through model for ManyToManyField
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'cost', 'verified', 'date')
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [TicketInline]

admin.site.register(Events)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Ticket)
admin.site.register(Contact)
admin.site.register(Jobs)
admin.site.register(Applicant)
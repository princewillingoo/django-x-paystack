from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'city', 'paid', 'updated',
    ]
    list_filter = ['paid', 'created', 'updated']
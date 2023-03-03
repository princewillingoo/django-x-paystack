from django import forms
from .models import Payment

class PaymentInitForm(forms.ModelForm):
    class Meta:
        model = Payment
        # model fields to include when creating form object
        fields = ['first_name', 'last_name', 'email', 'amount' ,'city']
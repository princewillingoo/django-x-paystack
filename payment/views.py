from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from .forms import PaymentInitForm

def payment_init(request):
    if request.method == 'POST':
        # get form data if POST request
        form = PaymentInitForm(request.POST)
        
        # validate form before saving
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()
            # set the payment in the current session
            request.session['payment_id'] = payment.id
            # message alert to confirm payment intializaton
            messages.success(request, "Payment Initialized Successfully." )
            # redirect user for payment completion
            return redirect(reverse('payment:process'))
    else:
    # render form if GET request
        form = PaymentInitForm()
    return render(request, 'payment/create.html', {'form': form})
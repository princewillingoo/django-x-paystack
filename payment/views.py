import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import requests
from .forms import PaymentInitForm
from django.shortcuts import get_object_or_404
from payment.models import Payment

# create the Paystack instance
api_key = settings.PAYSTACK_TEST_SECRETE_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

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


def payment_process(request):
    # retrive the payment_id we'd set in the djago session ealier
    payment_id = request.session.get('payment_id', None)
    # using the payment_id, get the database object
    payment = get_object_or_404(Payment, id=payment_id)
    # retrive payment amount 
    amount = payment.get_amount()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:success'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))
        
        # metadata to pass additional data that 
        # the endpoint doesn't accept naturally.
        metadata= json.dumps({"payment_id":payment_id,  
                              "cancel_action":cancel_url,   
                            })

        # Paystack checkout session data
        session_data = {
            'email': payment.email,
            'amount': int(amount),
            'callback_url': success_url,
            'metadata': metadata
            }
                
        headers = {"authorization": f"Bearer {api_key}"}
        # API request to paystack server
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()
        if response["status"] == True :
            # redirect to Paystack payment form
            try:
                redirect_url = response["data"]["authorization_url"]
                return redirect(redirect_url, code=303)
            except:
                pass
        else:
            return render(request, 'payment/process.html', locals())
    else:
        return render(request, 'payment/process.html', locals())
    
###previous code###

def payment_success(request):

    # retrive the payment_id we'd set in the django session ealier
    payment_id = request.session.get('payment_id', None)#new
    # using the payment_id, get the database object
    payment = get_object_or_404(Payment, id=payment_id)#new
    
    # retrive the query parameter from the request object
    ref = request.GET.get('reference', '')#new
    # verify transaction endpoint
    url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)#new
    
    # set auth headers
    headers = {"authorization": f"Bearer {api_key}"}#new
    r = requests.get(url, headers=headers)#new
    res = r.json()#new
    res = res["data"]

    # verify status before setting payment_ref
    if res['status'] == "success":  # new
        # update payment payment reference
        payment.paystack_ref = ref #new
        payment.save()#new
    
    return render(request, 'payment/success.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
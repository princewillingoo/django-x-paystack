from django.urls import path
from . import views

from payment import webhooks as wh # new

app_name = 'payment'

urlpatterns = [
    path('', views.payment_init, name='create'),
    path('process/', views.payment_process, name='process'),
    path('success/', views.payment_success, name='success'), 
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', wh.stack_webhook, name='stack-webhook'),# new
]
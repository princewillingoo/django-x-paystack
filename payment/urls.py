from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment_init, name='create'),
    path('process/', views.payment_process, name='process'), #new
    path('success/', views.payment_success, name='success'), #new
    path('canceled/', views.payment_canceled, name='canceled'), #new
]
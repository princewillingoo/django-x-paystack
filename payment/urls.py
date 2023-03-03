from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment_init, name='create'),
]
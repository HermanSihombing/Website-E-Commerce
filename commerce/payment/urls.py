from django.urls import path
from . import views

urlpatterns = [
    path('pembayaran', views.PreparePayment, name='checkout'),
    path('hasil-pembayaran', views.ProsesPayment, name='proses-pembayaran'),

]
from django.urls import path
from . import views

app_name = 'kupon'

urlpatterns = [
    path('disc/', views.kupon_disk, name='disc')
]
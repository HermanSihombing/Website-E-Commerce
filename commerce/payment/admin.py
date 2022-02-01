from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'nama', 'amount', 'timestamp','nohp', 'email', 'alamat']
    list_filter = ['nama', 'amount', 'timestamp']
    search_fields = ['nama', 'alamat']

from django.contrib import admin
from .models import Kupon

@admin.register(Kupon)
class KuponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'diskon', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

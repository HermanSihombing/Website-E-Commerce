from django.contrib import admin
from .models import Category, Product, Reviewed

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Reviewed)
class ReviewedAdmin(admin.ModelAdmin):
    list_display = ('nama', 'comment','rating','product', 'created')
    list_filter = ('product', 'created', 'rating')
    search_fields = ('nama', 'product', 'comment')
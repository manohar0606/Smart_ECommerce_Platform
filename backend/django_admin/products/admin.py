from django.contrib import admin
from .models import Product
# Register your models here.
admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category')
    

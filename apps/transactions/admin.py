from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'amount', 'category', 'date', 'description']
    list_filter = ['type', 'category', 'date']
    search_fields = ['description', 'notes']
    date_hierarchy = 'date'

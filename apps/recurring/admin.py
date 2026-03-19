from django.contrib import admin
from .models import RecurringTransaction

@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'type', 'amount', 'frequency', 'next_date', 'is_active']
    list_filter = ['type', 'frequency', 'is_active']
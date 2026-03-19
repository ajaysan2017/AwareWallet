from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'limit_amount', 'month', 'percentage_used', 'alert_level']
    list_filter = ['month', 'category']
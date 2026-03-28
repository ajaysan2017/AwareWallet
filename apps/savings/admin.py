from django.contrib import admin
from .models import SavingsGoal

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_name', 'target_amount', 'current_amount', 'percentage_complete', 'deadline', 'is_completed']
    list_filter = ['is_completed']

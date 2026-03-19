from rest_framework import serializers
from .models import SavingsGoal

class SavingsGoalSerializer(serializers.ModelSerializer):
    percentage_complete = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()

    class Meta:
        model = SavingsGoal
        fields = ['id', 'goal_name', 'target_amount', 'current_amount',
                  'percentage_complete', 'remaining_amount', 'deadline',
                  'icon', 'color', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']

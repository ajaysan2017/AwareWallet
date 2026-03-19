from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    spent_amount = serializers.ReadOnlyField()
    percentage_used = serializers.ReadOnlyField()
    alert_level = serializers.ReadOnlyField()

    class Meta:
        model = Budget
        fields = ['id', 'category', 'limit_amount', 'month',
                  'spent_amount', 'percentage_used', 'alert_level', 'created_at']
        read_only_fields = ['id', 'created_at']
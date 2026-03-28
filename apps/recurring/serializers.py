from rest_framework import serializers
from .models import RecurringTransaction

class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = ['id', 'type', 'amount', 'category', 'description',
                  'frequency', 'next_date', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

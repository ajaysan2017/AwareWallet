from rest_framework import serializers
from .models import Transaction
from apps.categories.serializers import CategorySerializer

class TransactionSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'category', 'category_detail',
                  'date', 'description', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']

from django import forms
from .models import RecurringTransaction
from apps.categories.models import Category

class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['type', 'amount', 'category', 'description', 'frequency', 'next_date', 'is_active']
        widgets = {
            'next_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = (
                Category.objects.filter(user=user) |
                Category.objects.filter(is_default=True)
            ).distinct()
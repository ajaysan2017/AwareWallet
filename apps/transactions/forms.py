"""
apps/transactions/forms.py
"""
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Transaction
from apps.categories.models import Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'date', 'description', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = (
                Category.objects.filter(user=user) |
                Category.objects.filter(is_default=True)
            ).distinct()
        self.fields['category'].required = True
        self.fields['description'].required = False
        self.fields['notes'].required = False

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise ValidationError('Amount is required.')
        if amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        if amount > 999999999:
            raise ValidationError('Amount is too large.')
        return round(amount, 2)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise ValidationError('Date is required.')
        today = timezone.now().date()
        min_date = today.replace(year=today.year - 10)
        if date < min_date:
            raise ValidationError('Date cannot be more than 10 years in the past.')
        max_date = today.replace(year=today.year + 1)
        if date > max_date:
            raise ValidationError('Date cannot be more than 1 year in the future.')
        return date

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) > 255:
            raise ValidationError('Description cannot exceed 255 characters.')
        return description

    def clean_notes(self):
        notes = self.cleaned_data.get('notes', '').strip()
        if len(notes) > 1000:
            raise ValidationError('Notes cannot exceed 1000 characters.')
        return notes

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        # Auto-set type based on category
        if category:
            cleaned_data['type'] = category.type
        else:
            cleaned_data['type'] = 'expense'
        return cleaned_data

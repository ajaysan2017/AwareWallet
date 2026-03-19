"""
apps/budgets/forms.py
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Budget
from apps.categories.models import Category
import datetime


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'month']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user                  # ← must be BEFORE super().__init__
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = (
                Category.objects.filter(user=user, type='expense') |
                Category.objects.filter(is_default=True, type='expense')
            ).distinct()

    def clean_limit_amount(self):
        amount = self.cleaned_data.get('limit_amount')
        if amount is None:
            raise ValidationError('Limit amount is required.')
        if amount <= 0:
            raise ValidationError('Limit amount must be greater than zero.')
        if amount > 999999999:
            raise ValidationError('Limit amount is too large.')
        return round(amount, 2)

    def clean_month(self):
        month = self.cleaned_data.get('month')
        if not month:
            raise ValidationError('Month is required.')
        # Force to first day of month
        month = month.replace(day=1)
        # Don't allow budgets more than 1 year in the past
        today = timezone.now().date()
        min_month = today.replace(year=today.year - 1, day=1)
        if month < min_month:
            raise ValidationError('Cannot create a budget more than 1 year in the past.')
        # Don't allow budgets more than 1 year in the future
        max_month = today.replace(year=today.year + 1, day=1)
        if month > max_month:
            raise ValidationError('Cannot create a budget more than 1 year in the future.')
        return month

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        month = cleaned_data.get('month')

        if category and month and self.user:
            # Check for duplicate budget — same user, category and month
            qs = Budget.objects.filter(
                user=self.user,
                category=category,
                month=month
            )
            # Exclude current instance when editing
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    f'A budget for "{category.name}" in '
                    f'{month.strftime("%B %Y")} already exists. '
                    f'Please edit the existing one instead.'
                )
        return cleaned_data
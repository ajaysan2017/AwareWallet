from django import forms
from django.core.exceptions import ValidationError
from .models import SavingsGoal


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['goal_name', 'target_amount', 'current_amount', 'deadline', 'color']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def clean_goal_name(self):
        name = self.cleaned_data.get('goal_name', '').strip()
        if not name:
            raise ValidationError('Goal name is required.')
        if len(name) < 2:
            raise ValidationError('Goal name must be at least 2 characters.')
        if len(name) > 150:
            raise ValidationError('Goal name cannot exceed 150 characters.')
        return name

    def clean_target_amount(self):
        amount = self.cleaned_data.get('target_amount')
        if amount is None:
            raise ValidationError('Target amount is required.')
        if amount <= 0:
            raise ValidationError('Target amount must be greater than zero.')
        return round(amount, 2)

    def clean_current_amount(self):
        amount = self.cleaned_data.get('current_amount')
        if amount is None:
            return 0
        if amount < 0:
            raise ValidationError('Current amount cannot be negative.')
        return round(amount, 2)

    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get('target_amount')
        current = cleaned_data.get('current_amount')
        if target and current and current > target:
            raise ValidationError(
                'Current amount cannot be greater than the target amount.'
            )
        return cleaned_data


class SavingsDepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        label='Add Amount'
    )

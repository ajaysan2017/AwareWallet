"""
apps/users/forms.py
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address.'
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        help_text='Enter your first name.'
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        help_text='Enter your last name.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        if not username.isalnum() and '_' not in username:
            raise ValidationError('Username can only contain letters, numbers and underscores.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError('First name can only contain letters.')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError('Last name can only contain letters.')
        return last_name.capitalize()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    def clean_username(self):
        email = self.cleaned_data.get('username', '').strip().lower()
        return email


CURRENCY_CHOICES = [
    ('USD', 'USD — US Dollar ($)'),
    ('EUR', 'EUR — Euro (€)'),
    ('GBP', 'GBP — British Pound (£)'),
    ('INR', 'INR — Indian Rupee (₹)'),
    ('JPY', 'JPY — Japanese Yen (¥)'),
    ('CAD', 'CAD — Canadian Dollar (CA$)'),
    ('AUD', 'AUD — Australian Dollar (A$)'),
    ('CHF', 'CHF — Swiss Franc (Fr)'),
    ('CNY', 'CNY — Chinese Yuan (¥)'),
    ('SEK', 'SEK — Swedish Krona (kr)'),
    ('NOK', 'NOK — Norwegian Krone (kr)'),
    ('MXN', 'MXN — Mexican Peso (MX$)'),
    ('SGD', 'SGD — Singapore Dollar (S$)'),
    ('AED', 'AED — UAE Dirham (د.إ)'),
]
class ProfileUpdateForm(forms.ModelForm):
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'currency', 'monthly_income', 'avatar']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        # Exclude current user from uniqueness check
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email is already in use by another account.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise ValidationError('First name is required.')
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError('First name can only contain letters.')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise ValidationError('Last name is required.')
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError('Last name can only contain letters.')
        return last_name.capitalize()

    def clean_currency(self):
        currency = self.cleaned_data.get('currency', '').strip().upper()
        valid_currencies = [
            'USD', 'EUR', 'GBP', 'INR', 'JPY', 'CAD',
            'AUD', 'CHF', 'CNY', 'SEK', 'NOK', 'MXN', 'SGD', 'AED'
        ]
        if currency not in valid_currencies:
            raise ValidationError(f'Invalid currency. Supported: {", ".join(valid_currencies)}')
        return currency

    def clean_monthly_income(self):
        income = self.cleaned_data.get('monthly_income')
        if income is not None and income < 0:
            raise ValidationError('Monthly income cannot be negative.')
        return income
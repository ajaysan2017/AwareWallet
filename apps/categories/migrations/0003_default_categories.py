"""Migration to add default categories."""

from django.db import migrations


def add_default_categories(apps, schema_editor):
    """Create default income and expense categories."""
    Category = apps.get_model('categories', 'Category')

    income_categories = [
        'Salary', 'Freelance', 'Investment Returns', 'Gift', 'Other Income'
    ]
    expense_categories = [
        'Food & Dining', 'Transport', 'Rent', 'Utilities',
        'Entertainment', 'Shopping', 'Health', 'Education',
        'Travel', 'Personal Care', 'Other Expense'
    ]

    for name in income_categories:
        Category.objects.get_or_create(
            name=name,
            type='income',
            user=None,
            defaults={'is_default': True, 'color': '#34d399'}
        )

    for name in expense_categories:
        Category.objects.get_or_create(
            name=name,
            type='expense',
            user=None,
            defaults={'is_default': True, 'color': '#6366f1'}
        )


def remove_default_categories(apps, schema_editor):
    """Remove default categories."""
    Category = apps.get_model('categories', 'Category')
    Category.objects.filter(is_default=True).delete()


class Migration(migrations.Migration):
    """Migration to seed default categories."""

    dependencies = [
        ('categories', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ]
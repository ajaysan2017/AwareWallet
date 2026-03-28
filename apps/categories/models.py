"""
apps/categories/models.py
"""
from django.db import models
from django.conf import settings


class Category(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True, blank=True,
        help_text="Null = default system category available to all users"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, default='tag', help_text="Icon name e.g. 'food', 'car'")
    color = models.CharField(max_length=7, default='#6366f1', help_text="Hex color e.g. #6366f1")
    is_default = models.BooleanField(default=False, help_text="System default category")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['type', 'name']
        unique_together = [('user', 'name', 'type')]

    def __str__(self):
        return f"{self.name} ({self.type})"

"""
apps/budgets/models.py
"""
from django.db import models
from django.conf import settings
from apps.categories.models import Category


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(help_text="First day of the month e.g. 2024-01-01")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'budgets'
        unique_together = [('user', 'category', 'month')]
        ordering = ['-month']

    def __str__(self):
        return f"{self.user} | {self.category.name} | {self.month.strftime('%b %Y')} | ${self.limit_amount}"

    @property
    def spent_amount(self):
        """Total spent in this category for this budget's month."""
        from apps.transactions.models import Transaction
        from django.db.models import Sum
        result = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='expense',
            date__year=self.month.year,
            date__month=self.month.month,
        ).aggregate(total=Sum('amount'))
        return result['total'] or 0

    @property
    def percentage_used(self):
        if self.limit_amount == 0:
            return 0
        return round((self.spent_amount / self.limit_amount) * 100, 1)

    @property
    def alert_level(self):
        """Returns: 'safe', 'warning', 'danger', or 'exceeded'"""
        pct = self.percentage_used
        if pct >= 100:
            return 'exceeded'
        elif pct >= 80:
            return 'danger'
        elif pct >= 50:
            return 'warning'
        return 'safe'

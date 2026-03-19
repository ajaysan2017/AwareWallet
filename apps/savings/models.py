"""
apps/savings/models.py
"""
from django.db import models
from django.conf import settings


class SavingsGoal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='savings_goals'
    )
    goal_name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    icon = models.CharField(max_length=50, default='piggy-bank')
    color = models.CharField(max_length=7, default='#10b981')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'savings_goals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.goal_name} — ${self.current_amount}/${self.target_amount}"

    @property
    def percentage_complete(self):
        if self.target_amount == 0:
            return 0
        return round((self.current_amount / self.target_amount) * 100, 1)

    @property
    def remaining_amount(self):
        return max(self.target_amount - self.current_amount, 0)